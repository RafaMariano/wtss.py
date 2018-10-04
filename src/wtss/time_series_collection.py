from src.wtss.time_series import time_series
import pandas as pd
import matplotlib.pyplot as pyplot


class time_series_collection:

    def __init__(self, time_series_collection):

        self.time_series_collection = []

        for time_series_ in time_series_collection:
            point = [time_series_['query']['longitude'], time_series_['query']['latitude']]
            self.time_series_collection.append([time_series(time_series_), point])

    def df(self):

        df = {}
        geo_pd_set = []

        for time_series_ in self.time_series_collection:
            coordinates = [time_series_[1][0], time_series_[1][1]]
            timeline = time_series_[0].timeline

            df['timeline'] = timeline

            attributes = time_series_[0].attributes()
            for attr in attributes:
                df[attr] = time_series_[0][attr]

            pd_obj = pd.DataFrame(df)
            geo_pd_set.append([coordinates, pd_obj])

        return geo_pd_set

    def __make_label__(self, attributes, point):
        # attr_aux = attributes
        attr_aux = []
        for index, attr in enumerate(attributes):
            attr_aux.append(str(point) + " - " + attr)
            # attr_aux[index] = point + " - " + attr

        return attr_aux

    def plot(self, df, attributes):


        # if not isinstance(df, pd.DataFrame):
        #     raise ValueError('The input object needs to be a Pandas DataFrame')
        #
        # if df.empty:
        #     raise ValueError('Empty DataFrame')

        axis = None
        for pos in range(0, len(df)):
            point = str(df[0][0][0]) + " " + str(df[0][0][1])
            label_ = self.__make_label__(attributes, point)
            axis = df[pos][1].plot('timeline', attributes, label=label_, ax=axis)

        pyplot.show()
