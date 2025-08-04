import datetime
import json
import sys
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import xgboost as xgb

from claims_pipeline.data_pipeline.data_collection.data_ingest import collect_from_database
from claims_pipeline.data_pipeline.data_preprocessing.data_preprocessing import preprocess_data
from claims_pipeline.training_pipeline.model_evaluation.model_evaluation import evaluate_model
from claims_pipeline.training_pipeline.model_training.cv_training import cv_train_model
from claims_pipeline.training_pipeline.model_training.initial_training import split_data_train_test, train_model
from claims_pipeline.utils.load_config_for_env import load_config_for_env
from claims_pipeline.utils.logger import Logger


def _step_metadata_init(config: Any) -> tuple[dict, str]:
    # Initialise run folder to save pipeline step outputs to.
    run_dir_folder = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
    run_dir = f"src/claims_pipeline/training_pipeline/pipeline.out/{run_dir_folder}"
    Path(run_dir).mkdir(mode=77777)
    metadata_dict = {
        "model_name": config.model_metadata.model_name,
        "model_version": config.model_metadata.model_version,
    }
    return metadata_dict, run_dir


def _step_data_collection() -> pd.DataFrame:
    logger.info("Starting data collection and preprocessing pipeline.")
    claims_dataset_df = collect_from_database(config.data_collection.query)
    return claims_dataset_df


def _step_data_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Data collection completed. Preprocessing data now.")
    claims_dataset_df_cleaned = preprocess_data(
        df,
        columns_to_drop=[
            "family_history_3",
            "employment_type",
        ],
    )
    return claims_dataset_df_cleaned


def _step_train_initial_model(df_cleaned: pd.DataFrame) -> tuple[xgb.XGBClassifier, dict, dict]:
    logger.info("Splitting data")
    split_data = split_data_train_test(data_df=df_cleaned, label_column=config.training.label_column)
    logger.info("Starting initial model training.")
    initial_model, eval_set_metrics_dict = train_model(split_data)
    logger.info("Model training completed successfully.")
    return initial_model, split_data, eval_set_metrics_dict


def _step_evaluate_model(model: xgb.XGBClassifier, data: dict):
    logger.info("Evaluating model")
    initial_training_metrics, initial_testing_metrics = evaluate_model(model, data)
    logger.info("Model evaluation completed")
    return initial_training_metrics, initial_testing_metrics


def _step_hyperparameter_tuning(data: dict, eval_dict: dict, model_artifact_dir: str) -> dict:
    best_paramaters = cv_train_model(data, eval_dict)
    return best_paramaters


def _step_train_final_model(data: dict, best_parameters: dict) -> xgb.XGBClassifier:
    logger.info("Training model using best found paramaters")
    # 6.1 Use parameters above to train new model using those parameters
    final_model, _ = train_model(data, model_params=best_paramaters)
    return final_model


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
        config = load_config_for_env(filename="training_pipeline.yml", env=env)
    except FileNotFoundError:
        logger.exception("Config not found")
        sys.exit(1)

    # 0.1 Metadata Init
    metadata_dict, run_dir = _step_metadata_init(config=config)
    # 1.1 Save Data so we don't have to query the database every time if pipeline fails
    claims_dataset_df = _step_data_collection()
    collect_data_path = f"{run_dir}/raw_claims_dataset.parquet"
    claims_dataset_df.to_parquet(
        collect_data_path,
        index=False,
    )
    logger.info("Parquet successfully saved to: %s", collect_data_path)
    # 2.1 Clean data
    claims_dataset_df_cleaned = _step_data_preprocessing(df=claims_dataset_df)
    # 2.2 Save Cleaned data
    clean_data_path = f"{run_dir}/cleaned_claims_dataset.parquet"
    claims_dataset_df_cleaned.to_parquet(
        clean_data_path,
        index=False,
    )

    logger.info("Parquet file saved successfully to: %s", clean_data_path)
    # 3.1 Split the data and train the initial model
    initial_model, split_data, eval_set_metrics_dict = _step_train_initial_model(df_cleaned=claims_dataset_df_cleaned)

    # 4.1 Evaluate Model

    initial_training_metrics, initial_testing_metrics = _step_evaluate_model(model=initial_model, data=split_data)

    # 4.2 Save Metrics locally.
    metadata_dict["initial_training_metrics"] = initial_training_metrics
    metadata_dict["initial_testing_metrics"] = initial_testing_metrics
    joblib.dump(initial_model, "src/model_artifacts/initial_model.gz")

    best_paramaters = _step_hyperparameter_tuning(
        data=split_data,
        eval_dict=eval_set_metrics_dict,
        model_artifact_dir=run_dir,
    )

    joblib.dump(best_paramaters, f"{run_dir}/best_paramaters.gz")

    final_model = _step_train_final_model(data=split_data, best_parameters=best_paramaters)
    joblib.dump(final_model, f"{run_dir}/final_model.gz")
    joblib.dump(final_model, "src/model_artifacts/final_model.gz")
