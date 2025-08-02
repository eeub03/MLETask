import joblib
import json
import sys
from claims_pipeline.src.utils.logger import Logger
from claims_pipeline.src.data_collection.data_ingest import collect_from_database
from claims_pipeline.src.data_preprocessing.data_preprocessing import preprocess_data
from claims_pipeline.src.model_training.initial_training import train_model
from claims_pipeline.src.model_training.cv_training import cv_train_model
from claims_pipeline.src.utils.load_config_for_env import load_config_for_env
from claims_pipeline.src.model_evaluation.model_evaluation import evaluate_model


if __name__ == "__main__":
    logger = Logger(__name__)
    args = sys.argv[1:]
    if len(args) < 1:
        logger.error(
            "No environment provided. Usage: uv run pipeline.py '<ENVIRONMENT>'"
        )
        sys.exit(1)
    if len(args) > 1:
        logger.warning(
            "Multiple arguments provided, only the first will be used as the environment"
        )
    env = args[0]
    try:
        str(args[0])
    except ValueError:
        logger.error("Invalid env passed. Please provide a valid environment string.")
        sys.exit(1)
    try:
        config = load_config_for_env(filename="pipeline.yml", env=env)
    except FileNotFoundError as e:
        logger.error(
            "Configuration file not found. Please check the path or Environment argument passed."
        )
        logger.error(f"Error loading configuration: {e}")
        sys.exit(1)

    # 1. Load data from database

    logger.info("Starting data collection and preprocessing pipeline.")
    claims_dataset_df = collect_from_database(config.data_collection.query)

    # 1.1 Save Data so we don't have to query the database every time if pipeline fails
    # TODO: If dataset is very large, we should consider using chunking to save it.

    # claims_dataset_df.to_parquet(
    #     "claims_pipeline/data/raw_claims_dataset.parquet", index=False
    # )

    # 2.1 Clean data
    logger.info("Data collection completed. Preprocessing data now.")
    claims_dataset_df_cleaned = preprocess_data(
        claims_dataset_df, columns_to_drop=["family_history_3", "employment_type"]
    )

    filename = "cleaned_claims_dataset.parquet"
    logger.info(
        "Data preprocessing completed. Saving cleaned data as parquet file: %s",
        filename,
    )
    # 2.2 Save Cleaned data

    # claims_dataset_df_cleaned.to_parquet(
    #     "claims_pipeline/data/" + filename, index=False
    # )

    logger.info(
        f"Parquet file saved successfully to claims_pipeline/data/ + {filename}  Pipeline completed successfully."
    )

    # 3.1 Train model
    logger.info("Starting initial model training.")
    # Build the evaluation set & metric list
    initial_model, split_data, eval_set_metrics_dict = train_model(
        claims_dataset_df_cleaned, need_splitting=True, label_column="claim_status"
    )
    logger.info("Model training completed successfully.")

    # 4.1 Evaluate Model

    initial_training_metrics, initial_testing_metrics = evaluate_model(
        initial_model, split_data
    )

    # 4.2 Save Metrics locally. Save Model Locally.
    # This enables us to reuse the model in inference pipelines.
    # joblib.dump(initial_model, "initial_model.joblib")
    # save_to_database(initial_training_metrics, table)
    # save_to_database(initial_testing_metrics, table)

    # Randomized GridSearch is very computationaly expensive, even with this small dataset so "caching" the results for integration testing.
    params_location = "claims_pipeline/data/params.gz"
    try:
        best_paramaters = joblib.load(params_location)
    except FileNotFoundError:
        # 5.1 Use Cross Validation to see if model performance can be improved.
        best_paramaters = cv_train_model(split_data, eval_set_metrics_dict)
        joblib.dump(best_paramaters, params_location, compress=1)
    logger.info("Best Parameters found")
    # 6.1 Use parameters above to train new model using those parameters
    final_model = train_model(
        split_data, need_splitting=False, model_params=best_paramaters
    )

    joblib.dump(final_model, "claims_pipeline/model_artifacts/model.gz")
