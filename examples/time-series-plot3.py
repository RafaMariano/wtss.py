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

import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from wtss import wtss

# The WTSS service is at: http://www.dpi.inpe.br/tws
w = wtss("http://www.dpi.inpe.br/tws")

# retrieve the time series for location (-54, -12)
ts = w.time_series("mod13q1_512", ["red", "nir"], -12.0, -54.0, start_date="2000-02-18", end_date="2006-01-01")

# get the list of values for the red time series
red_values = wtss.values(ts, "red")

# get the date list
timeline = wtss.timeline(ts, "%Y-%m-%d")

fig, ax = pyplot.subplots()

ax.plot(timeline, red_values, 'o-')

xfmt = mdates.DateFormatter('%d-%m-%Y')
ax.xaxis.set_major_formatter(xfmt)

fig.autofmt_xdate()

pyplot.show()



