from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
# from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):
    # get the execution datetime from runtime variable
    now = kwargs.get("execution_date")
    now_fpath = now.strftime("%Y/%m/%d")

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'datatalks-mage-bucket'
    object_key = f'{now_fpath}/daily_trips.parquet'

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        data,
        bucket_name,
        object_key,
    )


