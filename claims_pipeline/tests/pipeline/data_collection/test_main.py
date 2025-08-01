import pytest
from claims_pipeline.src.data_collection.data_processing import run_data_collection
import yaml
import os
import pandas as pd
import pandera

@pytest.fixture
def mock_data_values():
    return yaml.safe_load(open("./tests/fixtures/mock_data_values.yaml", encoding="utf-8").read())


def test_run_data_collection(mock_data_values):
    query = "SELECT * FROM CLAIMS.DS_DATASET"
    run_data_collection(query)
    
    # Check if the file is created
    filename = "cleaned_claims_dataset.parquet"
    assert os.path.exists(filename), f"File {filename} was not created."
    
    df = pd.read_parquet(filename)
    assert not df.empty, "The DataFrame should not be empty after processing."
    
    # Clean up the file after test
    os.remove(filename)