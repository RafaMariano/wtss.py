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
#  e-sensing team at <esensning-team@dpi.inpe.br>.
#

import json
import urllib2

class wtss:
    """This class implement the WTSS API for Python.

    Example:

        The code snippet below shows how to retrive a time series for location (-12, -54)::

            from wtss import wtss

            w = wtss("http://www.dpi.inpe.br/tws")

            cv_list = w.list_coverages()

            print(cv_list)

            cv_scheme = w.describe_coverage("mod13q1_512")

            print(cv_scheme)

            ts = w.time_series("mod13q1_512", ["red", "nir"], -12.0, -54.0, "", "")

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
            { 'coverges' : ['cv1', 'cv2', ... 'cvn'] }

        """
        return self._request("%s/wtss/list_coverages" % self.host)

    def describe_coverage(self, cv_name):
        """Returns the metadata of a given coverage.

        Args:
            cv_name (str): the coverage name whose schema you are interested in.

        Returns:
            dict: a JSON document with some metadata about the informed coverage.
        """
        return self._request("%s/wtss/describe_coverage?name=%s" % (self.host, cv_name))

    def time_series(self, cv_name, attributes, latitude, longitude, start_date = None, end_date = None):
        """Retrieve the time series for a given location and time interval.

        Args:

            cv_name (str): the coverage name whose time serie you are interested in.
            attributes(list): the list of attributes you are interested in to have the time series.
            latitude(double): latitude in degrees with the datum WGS84 (EPSG 4326).
            longitude(double): longitude in degrees with the datum WGS84 (EPSG 4326).
            start_date(str, optional): start date.
            ebd_date(str, optional): end date.

        Raises:
            ValueError: if latitude or longitude is out of range.
        """

        if (latitude < -90.0) or (latitude > 90.0):
            raise ValueError('latitude is out-of range!')

        if (longitude < -180.0) or (longitude > 180.0):
            raise ValueError('longitude is out-of range!')

        query_str = "%s/wtss/time_series?coverage=%s&attributes=%s&latitude=%f&longitude=%f" % (self.host, cv_name, ",".join(attributes), latitude, longitude)

        if start_date and end_date:
            query_str += "&start=%s&end=%s" % (start_date, end_date)

        return self._request(query_str)

    def _request(self, uri):

        resource = urllib2.urlopen(uri)

        doc = resource.read()

        return json.loads(doc)
