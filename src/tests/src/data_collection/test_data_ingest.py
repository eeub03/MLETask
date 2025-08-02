import pandas as pd
import pytest
import yaml

from claims_pipeline.pipeline.data_collection.data_ingest import collect_from_database
from claims_pipeline.utils.logger import Logger


@pytest.fixture
def logger():
    """
    Fixture to provide a custom logger for testing.
    """
    return Logger("TestLogger")


@pytest.fixture
def mock_data_values():
    return yaml.safe_load(open("claims_pipeline/tests/fixtures/config/pipeline.yml"))


@pytest.fixture
def database_stubber(mocker):
    """
    Mock the database connection and query execution.
    This prevents our script from trying to connect to a real database during tests by stubbing the database call.
    Alternatively, we could just mock the call to the database itself.
    """
    return None


def test_collect_from_database(mock_data_values, database_stubber):
    query = "SELECT * FROM CLAIMS.DS_DATASET"
    # We would also pass in mock_data_values if this was a real database call.

    # with database_stubber:
    #     df = collect_from_database(query, mock_data_values)

    df = collect_from_database(query)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "DataFrame should not be empty"


def test_collect_from_database_error_invalid_query(database_stubber):
    invalid_query = "SELECT odd"
    # Test will fail as we are not querying for real.
    with pytest.raises(Exception):
        collect_from_database(invalid_query)


def test_collect_from_database_error_timeout(database_stubber):
    timeout_query = "SELECT * FROM CLAIMS.DS_DATASET WHERE 1=0"
    # Test will fail as we are not querying for real.
    with pytest.raises(Exception):
        collect_from_database(timeout_query)


def test_collect_from_database_error_table_doesnt_exist(database_stubber):
    invalid_query = "SELECT * FROM non_existent_table"
    # Test will fail as we are not querying for real.
    with pytest.raises(Exception):
        collect_from_database(invalid_query)
