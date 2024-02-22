import argparse
import gzip
import os
import shutil
import pandas as pd

from sqlalchemy import create_engine
from time import time


def main(args):
    db_user = args.user
    db_password = args.password
    db_host = args.host
    db_port = args.port
    db_name = args.db_name
    db_table = args.table_name
    csv_url = args.url

    # create database connection and connect
    db_conn = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    db_conn.connect()

    # download data file, we expect this to be in zip format '.gz'
    os.system(f"wget -O output.csv.gz {csv_url}")

    df_iter = pd.read_csv("output.csv.gz", compression="gzip", iterator=True, chunksize=100000)

    df = next(df_iter)

    # convert text datetime columns to datetime
    #TODO: change to parse dates option
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # create db table using the headers from csv file
    df.head(n=0).to_sql(name=db_table, con=db_conn, if_exists="replace")

    # append 1st chunk of data from csv file to newly created table
    df.to_sql(name=db_table, con=db_conn, if_exists="append")

    # append remaing rows of data from csv file
    while True:
        try:
            # start time check
            t_start = time()

            df = next(df_iter)

            # convert text datetime columns to datetime
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            # add next chunk of data from csv file
            df.to_sql(name=db_table, con=db_conn, if_exists="append")

            # stop time check
            t_end = time()
            time_elapsed = t_end - t_start

            print(f"data chunk successfully added, time taken - {time_elapsed:.3f}")
        except StopIteration:
            print("end of file, no more data to add")
            break


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Ingest CSV file data into postgres DB")
    parser.add_argument("--user", help="database username")
    parser.add_argument("--password", help="password for database user")
    parser.add_argument("--host", help="database hostname")
    parser.add_argument("--port", help="database port number")
    parser.add_argument("--db_name", help="database name")
    parser.add_argument("--table_name", help="database table")
    parser.add_argument("--url", help="url for the csv file")

    args = parser.parse_args()

    main(args)