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

import numpy
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
from wtss import wtss

# The WTSS service is at: http://www.dpi.inpe.br/tws
w = wtss("http://www.dpi.inpe.br/tws")

# retrieve the time series for location (-54, -12)
ts = w.time_series("mod13q1_512", "red", -12.0, -54.0, start_date="2000-02-18", end_date="2006-01-01")

# prepare chart parameters
num_values = len(ts.timeline)

# create an evenly spaced array of values within interval: [0, num_values)
indices = numpy.arange(num_values)

# callback
def format_date(x, pos = None):
    idx = numpy.clip(int(x + 0.5), 0, num_values - 1)

    d = ts.timeline[idx]

    sd = d.strftime("%d-%m-%Y")

    return sd

fig, ax = pyplot.subplots()

ax.plot(indices, ts["red"], 'o-')

ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

fig.autofmt_xdate()

pyplot.show()



