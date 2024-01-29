import gzip
import os
import shutil

url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

os.system(f"wget -O output.csv.gz {url}")

with gzip.open("output.csv.gz", "rb") as f_in:
    with open("output.csv", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
