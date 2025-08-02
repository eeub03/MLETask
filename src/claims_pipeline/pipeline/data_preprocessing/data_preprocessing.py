import pandas as pd

from claims_pipeline.schemas.data_preprocessing.data_processing import InputSchema
from claims_pipeline.utils.logger import Logger

logger = Logger(__name__)


def preprocess_data(df: pd.DataFrame, columns_to_drop: list[str]) -> pd.DataFrame:
    df_cleaned = df.drop(columns=columns_to_drop)

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
        df_cleaned[column] = df_cleaned[column].astype("category")

    InputSchema.validate(df_cleaned)

    return df_cleaned
