import pandas as pd
import matplotlib.pyplot as pyplot


class time_series:
    """This class is a proxy for the result of a time_series query in WTSS.

    Example:

        The code snippet below shows how to retrieve a time series for location (latitude = -12, longitude = -54):

            from wtss import wtss

            w = wtss("http://www.dpi.inpe.br/tws")

            ts = w.time_series(coverage = "mod13q1_512", attributes = ["red", "nir"], latitude = -12.0, longitude = -54.0)

            print(ts["red"])

            print(ts["nir"])

            print(ts.timeline())


    Attributes:

        attributes (list): the list of attributes from a time_series query to a WTSS server.
        timeline (list): the timeline from a time_series query to a WTSS server.
    """

    def __init__(self, time_series):
        """Initializes a timeseries object from a WTSS time_series query.

        Args:
            time_series (dict): a response from a time_series query to a WTSS server.
        """

        self.doc = time_series

        self.attributes_ = {}

        for attr in time_series["result"]["attributes"]:
            name = attr["attribute"]
            values = attr["values"]
            self.attributes_[name] = values

        self.timeline = time_series["result"]["timeline"]

    def __getitem__(self, item):
        """Returns the list of values for a given attribute.

        Args:
            item (str): the name of an attribute.

        Returns:
            (list): values.
        """
        return self.attributes_[item]

    def attributes(self):
        """Returns a list with attribute names.

        Returns:
            (list): a list of strings with the attribute names.
        """

        return self.attributes_.keys()

    def df(self):

        df = {'timeline': self.timeline}

        for attr in self.attributes():
            df[attr] = self.attributes_[attr]

        pd_obj = pd.DataFrame(df)
        return pd_obj

    def plot(self, df, attributes):

        if not isinstance(df, pd.DataFrame):
            raise ValueError('The input object needs to be a Pandas DataFrame')

        if df.empty:
            raise ValueError('Empty DataFrame')

        df.plot('timeline', attributes)
        pyplot.show()
