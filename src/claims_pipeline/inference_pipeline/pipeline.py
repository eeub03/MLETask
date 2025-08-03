import sys
from typing import Any

import pandas as pd

from claims_pipeline.data_pipeline.data_collection.data_ingest import collect_from_database
from claims_pipeline.data_pipeline.data_preprocessing.data_preprocessing import preprocess_data
from claims_pipeline.inference_pipeline.inference.inference import batch_inference
from claims_pipeline.utils.load_config_for_env import load_config_for_env
from claims_pipeline.utils.logger import Logger

logger = Logger(__name__)


def _step_data_collection(config: Any):
    logger.info("Starting data collection and preprocessing pipeline.")

    claims_dataset_df = collect_from_database(config.data_collection.query)
    return claims_dataset_df


def _step_data_cleaning(df: pd.DataFrame):
    logger.info("Data collection completed. Preprocessing data now.")
    claims_dataset_df_cleaned = preprocess_data(
        df,
        columns_to_drop=[
            "family_history_3",
            "employment_type",
        ],
    )
    return claims_dataset_df_cleaned


def _step_batch_inference(model_path, data):
    batch_inference(model_path, data)


if __name__ == "__main__":
    logger = Logger(__name__)
    args = sys.argv[1:]
    if len(args) < 1:
        logger.error("No environment provided. Usage: uv run pipeline.py '<ENVIRONMENT>'")
        sys.exit(1)
    if len(args) > 1:
        logger.warning("Multiple arguments provided, only the first will be used as the environment")
    env = args[0]
    try:
        str(args[0])
    except ValueError:
        logger.exception("Invalid env passed. Please provide a valid environment string.")
        sys.exit(1)
    try:
        config = load_config_for_env(filename="pipeline.yml", env=env)
    except FileNotFoundError:
        sys.exit(1)
