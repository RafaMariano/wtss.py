#
#   Copyright (C) 2014 National Institute For Space Research (INPE) - Brazil.
#
#  This file is part of Python Client API for Web Time Series Service.
#
#  Web Time Series Service for Python is free software: you can
#  redistribute it and/or modify it under the terms of the
#  GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License,
#  or (at your option) any later version.
#
#  Web Time Series Service for Python is distributed in the hope that
#  it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Web Time Series Service for Python. See LICENSE. If not, write to
#  e-sensing team at <esensing-team@dpi.inpe.br>.
#

import geojson
import json
import shapely.wkt
import shapely.geometry
from datetime import datetime
from .time_series import time_series
from .time_series_collection import time_series_collection

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
    from urllib import parse, request


except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, parse, quote



class wtss:
    """This class implements the WTSS API for Python. See https://github.com/e-sensing/eows for more information on WTSS.

    Example:

        The code snippet below shows how to retrieve a time series for location (latitude = -12, longitude = -54):

            from wtss import wtss

            w = wtss("http://www.dpi.inpe.br/tws")

            ts = w.time_series(coverage = "mod13q1_512", attributes = ["red", "nir"], latitude = -12.0, longitude = -54.0)

            print(ts)

    Attributes:

        host (str): the WTSS server URL.
    """

    def __init__(self, host):
        """Create a WTSS client attached to the given host address (an URL).

        Args:
            host (str): the server URL.
        """
        self.host = host

    def list_coverages(self):
        """Returns the list of all available coverages in the service.

        Returns:
            dict: with a single key/value pair.

            The key named 'coverages' is associated to a list of str:
            { 'coverages' : ['cv1', 'cv2', ..., 'cvn'] }

        """
        return self._request("%s/wtss/list_coverages" % self.host)

    def describe_coverage(self, cv_name):
        """Returns the metadata of a given coverage.

        Args:
            cv_name (str): the coverage name whose schema you are interested in.

        Returns:
            dict: a JSON document with some metadata about the informed coverage.
        """
        result = self._request("%s/wtss/describe_coverage?name=%s" % (self.host, cv_name))
        attrs = dict()
        for attr in result['attributes']:
            attrs[attr['name']] = attr
        result['attributes'] = attrs
        return result

    def time_series(self, coverage, attributes, wkt=None, latitude=None, longitude=None, start_date=None, end_date=None):
        """Retrieve the time series for a given location and time interval.

        Args:

            coverage (str): the coverage name whose time series you are interested in.
            attributes(list, tuple, str): the list, tuple or string of attributes you are interested in to have the time series.
            wkt(str, optional if (latitude != None or longitude != None)): well-know text that represents a geometry.
            latitude(double, optional if (wkt != None)): latitude in degrees with the datum WGS84 (EPSG 4326).
            longitude(double, optional if (wkt != None)): longitude in degrees with the datum WGS84 (EPSG 4326).
            start_date(str, optional): start date.
            end_date(str, optional): end date.

        Raises:
            ValueError: if latitude or longitude is out of range or any mandatory parameter is missing.
            Exception: if the service returns a expcetion
        """

        data = {}

        if not coverage:
            raise ValueError("Missing coverage name.")

        if not attributes:
            raise ValueError("Missing coverage attributes.")

        if type(attributes) in [list, tuple]:
            attributes = ",".join(attributes)
        elif not type(attributes) is str:
            raise ValueError('attributes must be a list, tuple or string')

        data["coverage"] = coverage
        data["attributes"] = attributes

        if latitude is None or longitude is None:
            if wkt is None:
                raise ValueError('Necessary a geometry!!! Wkt or coordinates')
            else:
                if isinstance(wkt, str):
                    wkt_ = shapely.wkt.loads(wkt)
                # elif isinstance(wkt, shapely.geometry.base.BaseGeometry):
                else:
                    wkt_ = wkt
        else:
            if (latitude < -90.0) or (latitude > 90.0):
                raise ValueError("latitude is out-of range!")

            if (longitude < -180.0) or (longitude > 180.0):
                raise ValueError("longitude is out-of range!")

            wkt_ = shapely.wkt.loads('POINT ( ' + str(latitude) + ' ' + str(longitude) + ' )')

        geojson_ = geojson.Feature(geometry=wkt_, properties={})
        data["geometry"] = geojson_["geometry"]

        coord = data["geometry"]["coordinates"]
        time_series_ = []

        if data["geometry"]["type"] == "Polygon":
            coord = coord[0]

        elif data["geometry"]["type"] == "Point":
            coord = [coord]

        for point in coord:
            doc = self._prepare_request(self.host ,coverage, attributes, point, start_date, end_date)

            tl = doc["result"]["timeline"]
            tl = self._timeline(tl, "%Y-%m-%d")

            doc["result"]["timeline"] = tl
            time_series_.append(doc)

        if len(time_series_) > 1:
            return time_series_collection(time_series_)

        return time_series(time_series_[0])

    @classmethod
    def _prepare_request(cls, host, coverage, attributes, point, start_date, end_date):
        query_str = "%s/wtss/time_series?coverage=%s&attributes=%s&latitude=%f&longitude=%f" % \
                    (host, coverage, attributes, point[0], point[1])

        if start_date:
            query_str += "&start_date={}".format(start_date)

        if end_date:
            query_str += "&end_date={}".format(end_date)

        doc = cls._request(query_str)

        if 'exception' in doc:
            raise Exception(doc["exception"])

        return doc

    @classmethod
    def _request(cls, uri, data=None):

        if data is not None:
            uri = request.Request(uri, data=str.encode(data))
        resource = urlopen(uri)

        doc = resource.read().decode('utf-8')
        return json.loads(doc)

    @classmethod
    def _timeline(cls, tl, fmt):
        """Convert a timeline from a string list to a Python datetime list.

        Args:
            tl (list): a list of strings from a time_series JSON document response.
            fmt (str): the format date (e.g. `"%Y-%m-%d`").

        Returns:
            list (datetime): a timeline with datetime values.
        """
        date_timeline = [datetime.strptime(t, fmt).date() for t in tl]

        return date_timeline

    @classmethod
    def values(cls, doc, attr_name):
        """Returns the time series values for the given attribute from a time_series JSON document response.

        Args:
            doc (dict): a dictionary from a time_series JSON document response.
            attr_name (str): the name of the attribute to retrieve its a time series.

        Returns:
            list: the time series for the given attribute.

        Raises:
            ValueError: if attribute name is not in the document.
        """

        attrs = doc["properties"]["time_series"]

        if attrs[attr_name] is None:
            raise ValueError("Time series for attribute '{0}' not found!".format(attr_name))

        return attrs[attr_name]