# Python Client API for Web Time Series Service

**WTSS** is a lightweight web service for handling remote sensing imagery as time series. Given a location and a time interval you can retrieve the according time series as a Python list of real values.

If you want to know more about WTSS service, visit the [Earth Observation Web Services homepage](https://github.com/e-sensing/eows).

There are also client APIs for other programming languages: **[R](https://github.com/e-sensing/wtss.r)**, **[JavaScript](https://github.com/e-sensing/wtss.js)**, and **[C++](https://github.com/e-sensing/wtss.cxx)**.

## Installing wtss.py

Please, open a shell script and try:
```bash
sudo pip install wtss
```

or
```bash
sudo easy_install wtss
```

## Building and installing wtss.py from source

**1.** Open a shell script and go to the folder ```src```.

**2.** In the shell, type:
```bash
$ sudo pip install .
```
That's it!

## Using wtss.py to retrieve the time series

Import the ```wtss``` class and then use it to create an objet to retrieve the time series as shown in the following example:

```python
from wtss import wtss

w = wtss("http://www.dpi.inpe.br/tws")

cv_list = w.list_coverages()

print(cv_list)

cv_scheme = w.describe_coverage("mod13q1_512")

print(cv_scheme)

ts = w.time_series("mod13q1_512", ("red", "nir"), -12.0, -54.0, "", "")

print(ts["red"])

print(ts["nir"])

print(ts.timeline)
```


If you want to plot a time series, you can write a code like:
```python
import matplotlib.pyplot as pyplot
import matplotlib.dates as mdates
from wtss import wtss

w = wtss("http://www.dpi.inpe.br/tws")

# retrieve the time series for location with longitude = -54, latitude =  -12
ts = w.time_series("mod13q1_512", "red", -12.0, -54.0, start_date="2001-01-01", end_date="2001-12-31")

fig, ax = pyplot.subplots()

ax.plot(ts.timeline, ts["red"], 'o-')

fig.autofmt_xdate()

pyplot.show()
```

The codesnippet above will result in a chart such as:

<img src="./images/ts_plot.png" alt="Time Series" style="width: 600px;"/>

More examples can be found in the examples directory.

## References

VINHAS, L.; QUEIROZ, G. R.; FERREIRA, K. R.; CÂMARA, G. [Web Services for Big Earth Observation Data](http://urlib.net/8JMKD3MGP3W34P/3N2U9JL). In: BRAZILIAN SYMPOSIUM ON GEOINFORMATICS, 17. (GEOINFO), 2016, Campos do Jordão, SP. Proceedings... 2016.
