import pandas as pd

STAR_RATING_MAP = {
    'One':      1,
    'Two':      2,
    'Three':    3,
    'Four':     4,
    'Five':     5
}

class Transformer():

    def __init__(self, df):
        self.__df = df
        self.__parse_df()

    def get_df(self):
        return self.__df

    def __parse_df(self):
        print('Formatting data...')
        self.__format_available()
        self.__format_category()
        self.__format_prices()
        self.__format_rating()

    def __format_rating(self):
        self.__df.replace({'rating': STAR_RATING_MAP}, inplace=True)
        self.__df.rating = self.__df.rating.astype('int64')

    def __format_category(self):
        self.__df.category.replace("\\n", "", regex=True, inplace=True)

    def __format_prices(self):
        self.__df.price_notax.replace("£", "", regex=True, inplace=True)
        self.__df.price_tax.replace("£", "", regex=True, inplace=True)
        self.__df.tax_value.replace("£", "", regex=True, inplace=True)
        self.__df.price_notax = self.__df.price_notax.astype('float64')
        self.__df.price_tax = self.__df.price_tax.astype('float64')
        self.__df.tax_value = self.__df.tax_value.astype('float64')

    def __format_available(self):
        self.__df.n_available = self.__df.n_available.str.extract('^.*\((\d+) available\)$').astype('int32')
        self.__df.n_available.fillna(0, inplace=True)

