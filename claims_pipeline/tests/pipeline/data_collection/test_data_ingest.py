import pytest
from claims_pipeline.src.data_collection.data_ingest import collect_from_database
import pandas as pd
import yaml

@pytest.fixture
def mock_data_values():
    return

def test_data_ingest_returns_dataframe():
    query = "SELECT * FROM CLAIMS.DS_DATASET"
    df = collect_from_database(query)
    assert isinstance(df, pd.DataFrame)
    



