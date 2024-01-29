#!/usr/bin/env python
# coding: utf-8

import argparse
import gzip
import shutil
import os
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

    # extract csv file and copy to local file
    # with gzip.open("output.csv.gz", "rb") as f_in:
    #     with open("output.csv", "wb") as f_out:
    #         shutil.copyfileobj(f_in, f_out)

    # df_iter = pd.read_csv("output.csv", iterator=True, chunksize=100000)
    df_iter = pd.read_csv("output.csv.gz", compression="gzip", iterator=True, chunksize=100000)

    df = next(df_iter)

    df.rename(columns={'PULocationID':'pu_location_id'})
    df.rename(columns={'RatecodeID':'ratecode_id'})
    df.rename(columns={'DOLocationID': 'do_location_id'})

    # convert text datetime columns to datetime
    # df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    # df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    # create db table using the headers from csv file
    df.head(n=0).to_sql(name=db_table, con=db_conn, if_exists="replace")

    # append 1st chunk of data from csv file to newly created table
    df.to_sql(name=db_table, con=db_conn, if_exists="append")

    while True:
        try:
            t_start = time()
            
            df = next(df_iter)
            # format timestamp columns
            # df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            # df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            
            # add next chunk of data from csv file
            df.to_sql(name=db_table, con=db_conn, if_exists="append")

            t_end = time()
            time_taken = t_end- t_start

            print(f"data chunk added and took {time_taken:.3f} seconds")
        except StopIteration:
            print("end of file, no more data to read")
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


    

