import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/gcp_creds.json"

bucket_name = "datatalks-mage-bucket"
project_id = "sodium-chalice-412103"
table_name = "green_taxi_gcs_data"
root_path = f"{bucket_name}/{table_name}"


@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """    
    # create pyarrow table by reading data
    table = pa.Table.from_pandas(data)

    # create GCS filesystem object, authorizes using GCS environment variables
    gcs = pa.fs.GcsFileSystem()

    # use pyarrow.parquet to write dataset to gcs
    # use pyarrow.parquet to write dataset to gcs
    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=["lpep_pickup_date"],
        filesystem=gcs
    )

