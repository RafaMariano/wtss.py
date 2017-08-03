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

import matplotlib.pyplot as pyplot
from wtss import wtss

w = wtss("http://www.dpi.inpe.br/tws")

# retrieve the time series for location (-54, -12) in the time interval [2000-02-18, 2000-12-31]
ts = w.time_series("mod13q1_512", ["red", "nir"], latitude=-12.0, longitude=-54.0, start_date="2000-02-18", end_date="2000-12-31")

fig, ax = pyplot.subplots()

ax.plot(ts.timeline, ts["red"], '-')

fig.autofmt_xdate()

pyplot.show()
