from scipy import stats
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV
from claims_pipeline.src.utils.logger import Logger

logger = Logger(__name__)


def cv_train_model(split_data: pd.DataFrame, eval_set_metrics_dict: dict):
    X_train, y_train = split_data["X_train"], split_data["y_train"]
    eval_metrics, eval_set = (
        eval_set_metrics_dict["eval_metrics"],
        eval_set_metrics_dict["eval_set"],
    )

    parameter_gridSearch = RandomizedSearchCV(
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

    parameter_gridSearch.fit(X_train, y_train, eval_set=eval_set, verbose=False)

    logger.info("Best parameters are: ", parameter_gridSearch.best_params_)

    return parameter_gridSearch.best_params_
