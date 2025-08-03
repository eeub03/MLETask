import numpy as np
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from claims_pipeline.utils.logger import Logger

rng = np.random.default_rng(1889)

logger = Logger(__name__)


def evaluate_model(
    model: xgb.XGBClassifier,
    split_data: dict[str, np.ndarray],
) -> tuple[dict, dict]:
    """Return metrics for training and testing data given a dict containing x_train, y_train, x_test and y_test."""
    X_train, y_train = split_data["X_train"], split_data["y_train"]
    training_metrics = _evaluate_training(X_train, y_train, model)

    X_test, y_test = split_data["X_test"], split_data["y_test"]
    testing_metrics = _evaluate_testing(X_test, y_test, model)

    return training_metrics, testing_metrics


def _evaluate_training(X_train: np.ndarray, y_train: np.ndarray, model: xgb.XGBClassifier) -> dict:
    training_model_metrics = _evaluate(X=X_train, y=y_train, model=model)
    logger.info("### Training Metrics ###")
    for key, value in training_model_metrics.items():
        if isinstance(value, float):
            logger.info("%s : %.4f", key, value)
        else:
            logger.info("%s : %s", key, value)
    return training_model_metrics


def _evaluate(X: np.ndarray, y: np.ndarray, model: xgb.XGBClassifier) -> dict:
    class_preds = model.predict(X)

    prob_preds = model.predict_proba(X)[:, 1]

    y = np.array(y)
    y = y.astype(int)
    yhat = np.array(class_preds)
    yhat = np.clip(np.round(yhat), np.min(y), np.max(y)).astype(int)

    data_kappa_score = round(cohen_kappa_score(yhat, y, weights="quadratic"), 2)

    log_loss_value = log_loss(y, prob_preds)
    accuracy = accuracy_score(y, class_preds)
    roc_auc = roc_auc_score(y, prob_preds)
    confusion_matrix_value = confusion_matrix(y, class_preds)

    model_metrics = {
        "accuracy": accuracy,
        "kappa_score": data_kappa_score,
        "roc_auc": roc_auc,
        "log_loss": log_loss_value,
        "confusion_matrix": confusion_matrix_value,
    }

    return model_metrics


def _evaluate_testing(X_test: np.ndarray, y_test: np.ndarray, model: xgb.XGBClassifier) -> dict:
    model_metrics = _evaluate(X=X_test, y=y_test, model=model)

    test_class_preds = model.predict(X_test)
    test_prob_preds = model.predict_proba(X_test)[:, 1]

    fpr, tpr, _ = roc_curve(y_test, test_prob_preds)
    random_fpr, random_tpr, _ = roc_curve(y_test, [0 for _ in range(len(y_test))])

    f1_score_value = f1_score(y_test, test_class_preds)
    precision = precision_score(y_test, test_class_preds)
    recall = recall_score(y_test, test_class_preds)

    test_model_metrics = {
        "f1_score": f1_score_value,
        "precision": precision,
        "recall": recall,
        "roc_curve": {
            "fpr": fpr,
            "tpr": tpr,
            "random_fpr": random_fpr,
            "random_tpr": random_tpr,
        },
    }
    full_test_model_metrics = model_metrics | test_model_metrics
    for key, value in full_test_model_metrics.items():
        if isinstance(value, float):
            logger.info("%s : %.4f", key, value)
        else:
            logger.info("%s : %s", key, value)

    return full_test_model_metrics
