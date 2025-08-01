from claims_pipeline.utils.logger import CustomLogger
import sys
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.preprocessing import MinMaxScaler
import string
from claims_pipeline.schemas.pipeline.processed_data import InputSchema
import pandera.pandas as pa

logger = CustomLogger("DataCollection")


def collect_from_database(query: str) -> pd.DataFrame:
    print(f"Executing: {query}")
    n_rows = 10_000
    n_features = 16
    features, labels = make_classification(
        n_samples=n_rows,
        n_features=16,
        n_informative=7,
        n_redundant=4,
        n_repeated=3,
        n_classes=2,
        class_sep=1.2,
        flip_y=0.035,  # Randomly invert y for added noise
        weights=[0.85, 0.15],
        random_state=1889,
    )
    df = pd.DataFrame(features, columns=[f"numeric_{i+1}" for i in range(n_features)])
    df.insert(value=labels, loc=0, column="claim_status")
    df = df.rename(
        columns={
            "numeric_1": "age",
            "numeric_2": "height_cm",
            "numeric_3": "weight_kg",
            "numeric_4": "income",
            "numeric_5": "financial_hist_1",
            "numeric_6": "financial_hist_2",
            "numeric_7": "financial_hist_3",
            "numeric_8": "financial_hist_4",
            "numeric_9": "credit_score_1",
            "numeric_10": "credit_score_2",
            "numeric_11": "credit_score_3",
            "numeric_12": "insurance_hist_1",
            "numeric_13": "insurance_hist_2",
            "numeric_14": "insurance_hist_3",
            "numeric_15": "insurance_hist_4",
            "numeric_16": "insurance_hist_5",
        }
    )
    df["age"] = MinMaxScaler(feature_range=(18, 95)).fit_transform(
        df["age"].values[:, None]
    )
    df["age"] = df["age"].astype("int")
    df["height_cm"] = MinMaxScaler(feature_range=(140, 210)).fit_transform(
        df["height_cm"].values[:, None]
    )
    df["height_cm"] = df["height_cm"].astype("int")
    df["weight_kg"] = MinMaxScaler(feature_range=(45, 125)).fit_transform(
        df["weight_kg"].values[:, None]
    )
    df["weight_kg"] = df["weight_kg"].astype("int")
    df["income"] = MinMaxScaler(feature_range=(0, 250_000)).fit_transform(
        df["income"].values[:, None]
    )
    df["income"] = df["income"].astype("int")
    df["credit_score_1"] = MinMaxScaler(feature_range=(0, 999)).fit_transform(
        df["credit_score_1"].values[:, None]
    )
    df["credit_score_1"] = df["credit_score_1"].astype("int")
    df["credit_score_2"] = MinMaxScaler(feature_range=(0, 700)).fit_transform(
        df["credit_score_2"].values[:, None]
    )
    df["credit_score_2"] = df["credit_score_2"].astype("int")
    df["credit_score_3"] = MinMaxScaler(feature_range=(0, 710)).fit_transform(
        df["credit_score_3"].values[:, None]
    )
    df["credit_score_3"] = df["credit_score_3"].astype("int")
    df["bmi"] = (df["weight_kg"] / ((df["height_cm"] / 100) ** 2)).astype("int")
    df["gender"] = np.where(
        df["claim_status"] == 0,
        np.random.choice([1, 0], size=(n_rows), p=[0.46, 0.54]),
        np.random.choice([1, 0], size=(n_rows), p=[0.52, 0.48]),
    )
    df["marital_status"] = np.random.choice(
        ["A", "B", "C", "D", "E", "F"],
        size=(n_rows),
        p=[0.2, 0.15, 0.1, 0.25, 0.15, 0.15],
    )
    df["occupation"] = np.random.choice(
        ["A", "B", "C", "D", "E", "F", "G"], size=(n_rows)
    )
    df["location"] = np.random.choice(list(string.ascii_uppercase), size=(n_rows))
    df["prev_claim_rejected"] = np.where(
        df["claim_status"] == 0,
        np.random.choice([1, 0], size=(n_rows), p=[0.08, 0.92]),
        np.random.choice([1, 0], size=(n_rows), p=[0.16, 0.84]),
    )
    df["known_health_conditions"] = np.random.choice(
        [1, 0], size=(n_rows), p=[0.06, 0.94]
    )
    df["uk_residence"] = np.random.choice([1, 0], size=(n_rows), p=[0.76, 0.24])
    df["family_history_1"] = np.random.choice([1, 0], size=(n_rows), p=[0.22, 0.78])
    df["family_history_2"] = np.random.choice([1, 0], size=(n_rows), p=[0.25, 0.75])
    df["family_history_3"] = np.random.choice(
        [1, None, 0], size=(n_rows), p=[0.12, 0.81, 0.07]
    )
    df["family_history_4"] = np.random.choice([1, 0], size=(n_rows), p=[0.27, 0.73])
    df["family_history_5"] = np.random.choice([1, 0], size=(n_rows), p=[0.31, 0.69])
    df["product_var_1"] = np.random.choice([1, 0], size=(n_rows), p=[0.38, 0.62])
    df["product_var_2"] = np.random.choice([1, 0], size=(n_rows), p=[0.55, 0.45])
    df["product_var_3"] = np.random.choice(
        ["A", "B", "C", "D"], size=(n_rows), p=[0.23, 0.28, 0.31, 0.18]
    )
    df["product_var_4"] = np.random.choice([1, 0], size=(n_rows), p=[0.76, 0.24])
    df["health_status"] = np.random.randint(1, 5, size=(n_rows))
    df["driving_record"] = np.random.randint(1, 5, size=(n_rows))
    df["previous_claim_rate"] = np.where(
        df["claim_status"] == 0,
        np.random.choice(
            [1, 2, 3, 4, 5], size=(n_rows), p=[0.48, 0.29, 0.12, 0.08, 0.03]
        ),
        np.random.choice(
            [1, 2, 3, 4, 5], size=(n_rows), p=[0.12, 0.28, 0.34, 0.19, 0.07]
        ),
    )
    df["education_level"] = np.random.randint(0, 7, size=(n_rows))
    df["income level"] = pd.cut(df["income"], bins=5, labels=False, include_lowest=True)
    df["n_dependents"] = np.random.choice(
        [1, 2, 3, 4, 5], size=(n_rows), p=[0.23, 0.32, 0.27, 0.11, 0.07]
    )
    df["employment_type"] = np.random.choice(
        [1, None, 0], size=(n_rows), p=[0.16, 0.7, 0.14]
    )

    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(columns=["family_history_3", "employment_type"], inplace=True)

    categorical_columns = [
        "gender",
        "marital_status",
        "occupation",
        "location",
        "prev_claim_rejected",
        "known_health_conditions",
        "uk_residence",
        "family_history_1",
        "family_history_2",
        "family_history_4",
        "family_history_5",
        "product_var_1",
        "product_var_2",
        "product_var_3",
        "health_status",
        "driving_record",
        "previous_claim_rate",
        "education_level",
        "income level",
        "n_dependents",
    ]

    for column in categorical_columns:
        df[column] = df[column].astype("category")
    try:
        InputSchema.validate(df)
    except pa.errors.SchemaError as e:
        logger.error("Data validation failed: %s", e)
        raise e

    return df


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        logger.error("No query provided. Usage: python main.py '<SQL_QUERY>'")
        sys.exit(1)
    if len(args) > 1:
        logger.warning(
            "Multiple arguments provided, only the first will be used as the query."
        )
    query = args[0]
    try:
        str(args[0])
    except ValueError:
        logger.error("Invalid query format. Please provide a valid SQL query string.")
        sys.exit(1)

    logger.info("Starting data collection and preprocessing pipeline.")
    claims_dataset_df = collect_from_database(query)

    logger.info("Data collection completed. Preprocessing data now.")
    claims_dataset_df_cleaned = preprocess_data(claims_dataset_df)

    filename = "cleaned_claims_dataset.parquet"
    logger.info(
        "Data preprocessing completed. Saving cleaned data as parquet file: %s",
        filename,
    )
    claims_dataset_df_cleaned.to_parquet("/data/" + filename, index=False)
