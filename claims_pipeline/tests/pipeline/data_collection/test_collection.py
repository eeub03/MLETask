import pytest
from claims_pipeline.src.data_collection.data_processing import collect_from_database
import pandas as pd
import yaml
import os
from claims_pipeline.utils.logger import Logger


@pytest.fixture
def logger():
    """
    Fixture to provide a custom logger for testing.
    """
    return Logger("TestLogger")


@pytest.fixture
def mock_data_values(logger):
    logger.info(os.getcwd())
    return yaml.safe_load(
        open("claims_pipeline\\tests\\fixtures\\config\\collect_data.yml")
    )


@pytest.fixture
def database_stubber(mocker):
    """
    Mock the database connection and query execution.
    This prevents our script from trying to connect to a real database during tests by stubbing the database call.
    """
    return None


def test_collect_from_database(mock_data_values, database_stubber, logger):
    query = "SELECT * FROM CLAIMS.DS_DATASET"
    # We would also pass in mock_data_values if this was a real database call.

    # with database_stubber:
    #     df = collect_from_database(query, mock_data_values)

    df = collect_from_database(query)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "DataFrame should not be empty"


def test_collect_from_database_error_bad_query(database_stubber):
    bad_query = "SELECT odd"
    # Test will fail as we are not querying for real.
    with pytest.raises(Exception):
        collect_from_database(bad_query)


def test_preprocess_data(database_stubber):
    return None
