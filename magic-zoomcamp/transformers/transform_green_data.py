if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    
    # transform the columns from camelcase to snake case
    data.columns = (data.columns
                    .str.replace("(?<=[a-z])(?=[A-Z])", "_", regex=True)
                    .str.lower()
                    )

    # create new column lpep_pickup_date
    data["lpep_pickup_date"] = data["lpep_pickup_datetime"].dt.date

    # update data to remove passenger_count = 0
    data = data[data["passenger_count"] > 0]

    # update data to remove passenger count
    data = data[data["trip_distance"] > 0]

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'


@test
def test_column_vendor_id_exists(output, *args):
    assert "vendor_id" in output.columns, "There is no vendor_id column"


@test
def test_no_zero_passenger_count(output, *args):
    assert output["passenger_count"].isin([0]).sum() == 0, "There are rides with 0 passengers"


@test
def test_no_zero_trip_distance_count(output, *args):
    assert output["trip_distance"].isin([0]).sum() == 0, "There are trips with 0 distance"
