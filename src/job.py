from ast import Load
import os
from datetime import date

from extractor import Extractor
from transformer import Transformer
from loader import Loader

TABLE_NAME = "book_info"
DB_SCHEMA = [
    'title',
    'rating',
    'category',
    'upc',
    'product_type',
    'price',
    'price_withtax',
    'tax_value',
    'available_number',
    'review_number',
    'date',
    'year',
    'month',
    'day'
]

def main():

    # Initializing xtractor and collecting raw data from web
    extractor = Extractor()
    raw_data = extractor.scrape_books(csv_stage=False)

    # Parsing raw data into transformer class (formatting + typing)
    transformed = Transformer(raw_data).get_df()

    # Adding today's date indication to the the df
    today = date.today()
    transformed['date'] = today.strftime("%Y-%m-%d")
    transformed['year'] = today.strftime("%Y")
    transformed['month'] = today.strftime("%m")
    transformed['day'] = today.strftime("%d")

    # Storing formatted data into PostgresSQL
    loader = Loader(transformed)
    loader.store_pg(TABLE_NAME, DB_SCHEMA)

if __name__ == '__main__':
    main()