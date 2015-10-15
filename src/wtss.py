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

    def __init__(self, host):
        self.host = host

    def list_coverages(self):
        return self.request("%s/wtss/list_coverages" % self.host)


    def describe_coverage(self, cv_name):
        return self.request("%s/wtss/describe_coverage?name=%s" % (self.host, cv_name))

    def time_series(self, cv_name, attributes, latitude, longitude, start_date, end_date):
        query_str = "%s/wtss/time_series?coverage=%s&attributes=%s&latitude=%f&longitude=%f" % (self.host, cv_name, ",".join(attributes), latitude, longitude)

        if start_date and end_date:
            query_str += "&start=%s&end=%s" % (start_date, end_date)

        return self.request(query_str)

    def request(self, uri):

        resource = urllib2.urlopen(uri)

        doc = resource.read()

        print doc

        return json.loads(doc)


if __name__ == '__main__':
    w = wtss("http://gribeiro1.dpi.inpe.br:7654")

    w.list_coverages()

    w.describe_coverage("mcd43a4")

    w.time_series("mcd43a4", ["b1", "b2"], -12.0, -54.0, "", "")

