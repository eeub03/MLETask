from claims_pipeline.schemas.data_preprocessing.data_processing import InputSchema
import pandera.pandas as pa
import pandas as pd
from claims_pipeline.src.utils.logger import Logger

logger = Logger(__name__)


def preprocess_data(df: pd.DataFrame, columns_to_drop: list) -> pd.DataFrame:
    df.drop(columns=columns_to_drop, inplace=True)

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
        logger.error(
            f"Data validation failed: {e}",
        )
        raise e

    return df
