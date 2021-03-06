import os

import pandas as pd
from sqlalchemy import create_engine

PG_URL_FORMAT = "postgresql://{}:{}@{}:{}/{}"

class Loader():

    """
    This class is able to store a Pandas Dataframe
    into a PostgreSQL table, creating a connection
    through credentials obtained from environment 
    variables.
    """


    def __init__(self, df):
        self.__df = df
        self.__conn = self.__create_conn()

    def store_pg(self, table, schema):
        """
        Given a formated and correctly typed Pandas Dataframe, a table,
        and the correct column names for the table, it stores
        all data from the dataframe into the PGSQL table.
        """
        print('Storing data to a postgresql table')
        df_to_store = self.__df.copy()
        df_to_store.columns = schema
        df_to_store.to_sql(table, self.__conn, index=False, if_exists='append')

    def __create_conn(self):
        pg_username = os.getenv("PG_USER")
        pg_password = os.getenv("PG_PASS")
        pg_host = os.getenv("PG_HOST")
        pg_port = os.getenv("PG_PORT")
        pg_db = os.getenv("PG_DB")
        conn_url = PG_URL_FORMAT.format(pg_username, pg_password, pg_host, pg_port, pg_db)
        return create_engine(conn_url)