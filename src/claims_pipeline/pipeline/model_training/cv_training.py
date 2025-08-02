import numpy as np
import xgboost as xgb
from scipy import stats
from sklearn.model_selection import RandomizedSearchCV

from claims_pipeline.utils.logger import Logger

logger = Logger(__name__)


def cv_train_model(split_data: dict[str, np.ndarray], eval_set_metrics_dict: dict[str, list]) -> dict:
    """Perform hyper parameter tuning to find the best parameters for the model using RandomSearchCV."""
    X_train, y_train = split_data["X_train"], split_data["y_train"]
    eval_metrics, eval_set = (
        eval_set_metrics_dict["eval_metrics"],
        eval_set_metrics_dict["eval_set"],
    )

    parameter_gridsearch = RandomizedSearchCV(
        estimator=xgb.XGBClassifier(
            objective="binary:logistic",
            eval_metric=eval_metrics,
            early_stopping_rounds=15,
            enable_categorical=True,
        ),
        param_distributions={
            "n_estimators": stats.randint(50, 500),
            "learning_rate": stats.uniform(0.01, 0.75),
            "subsample": stats.uniform(0.25, 0.75),
            "max_depth": stats.randint(1, 8),
            "colsample_bytree": stats.uniform(0.1, 0.75),
            "min_child_weight": [1, 3, 5, 7, 9],
        },
        cv=5,
        n_iter=100,
        verbose=False,
        scoring="roc_auc",
    )

    parameter_gridsearch.fit(X_train, y_train, eval_set=eval_set, verbose=False)  # type: ignore

    logger.info("Best parameters are: ", parameter_gridsearch.best_params_)

    return parameter_gridsearch.best_params_
