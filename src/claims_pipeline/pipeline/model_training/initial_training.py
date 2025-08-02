import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

from claims_pipeline.utils.logger import Logger

logger = Logger(__name__)


def train_model(
    data: dict[str, np.ndarray],
    model_params: dict | None = None,
) -> tuple[xgb.XGBClassifier, dict[str, list]]:
    """Take in already split up data and train an xgboost model on it."""
    X_train, y_train = data["X_train"], data["y_train"]
    X_test, y_test = data["X_test"], data["y_test"]

    # Build the evaluation set & metric list
    eval_set = [(X_train, y_train)]
    eval_metrics = ["auc", "rmse", "logloss"]

    eval_set_metrics_dict = {"eval_set": eval_set, "eval_metrics": eval_metrics}

    model = xgb.XGBClassifier(
        objective="binary:logistic",
        eval_metric=eval_metrics,
        enable_categorical=True,
    )
    if model_params:
        model.set_params(**model_params)

    model.fit(X_test, y_test, eval_set=eval_set, verbose=10)

    return model, eval_set_metrics_dict


def split_data_train_test(
    data_df: pd.DataFrame,
    label_column: str,
    test_size: float = 0.2,
    random_state: int = 1889,
) -> dict[str, np.ndarray]:
    """Validate and Split up data into X_train, X_Test, y_train, y_test for model training."""
    logger.info("Validating DataFrame schema...")
    # Pandera schema validation goes here

    # Placeholder for model training logic
    logger.info("Training model...")
    # Separate the Dataframe into labels and features
    X, y = (
        data_df.drop(label_column, axis=1),
        data_df[[label_column]],
    )

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    split_data = {
        "X_train": X_train,
        "y_train": y_train,
        "X_test": X_test,
        "y_test": y_test,
    }
    return split_data
