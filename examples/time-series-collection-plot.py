from src.wtss import wtss
from shapely.geometry import MultiPoint

w = wtss("http://www.esensing.dpi.inpe.br")

cv_scheme = w.describe_coverage("MOD13Q1")

geom = MultiPoint([(-10.124, -46.677), (-9.712, -47.233)])

ts = w.time_series("MOD13Q1", ("ndvi"), geom)

ndvi = ts.df()

ts.plot(ndvi, ['ndvi'])