import pytest
import yaml

from claims_pipeline.training_pipeline.data_preprocessing.data_preprocessing import preprocess_data


@pytest.fixture
def mock_data_values(logger):
    return yaml.safe_load(open("claims_pipeline/tests/fixtures/config/pipeline.yml"))


@pytest.fixture
def sample_dataframe():
    # Create a sample DataFrame for testing
    data = {""}


@pytest.fixture
def sample_invalid_schema_dataframe():
    # Create an invalid DataFrame for testing schema validation
    data = {""}


def test_preprocess_data(mock_data_values):
    return None
