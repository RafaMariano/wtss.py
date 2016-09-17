# Python Client API for Web Time Series Service

**WTSS** is a lightweight web service for handling remote sensing imagery as time series. Given a location and a time interval you can retrieve the according time series as a Python list of real values.

If you want to know more abot WTSS service, visit the [TerraLib GeoWeb Services homepage](https://github.com/e-sensing/tws).

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

ts = w.time_series("mod13q1_512", ["red", "nir"], -12.0, -54.0, "", "")

print(ts)
```

