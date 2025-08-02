# from sklearn.datasets import *
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
import xgboost as xgb
import numpy as np
from claims_pipeline.src.utils.logger import Logger

np.random.seed(1889)

logger = Logger(__name__)


def evaluate_model(
    model: xgb.XGBClassifier,
    split_data: dict,
) -> tuple[dict, dict]:

    X_train, y_train = split_data["X_train"], split_data["y_train"]
    training_metrics = _evaluate_training(X_train, y_train, model)

    X_test, y_test = split_data["X_test"], split_data["y_test"]
    testing_metrics = _evaluate_testing(X_test, y_test, model)

    return training_metrics, testing_metrics


def _evaluate_training(X_train, y_train, model) -> dict:
    train_class_preds = model.predict(X_train)

    train_prob_preds = model.predict_proba(X_train)[:, 1]

    y = np.array(y_train)
    y = y.astype(int)
    yhat = np.array(train_class_preds)
    yhat = np.clip(np.round(yhat), np.min(y), np.max(y)).astype(int)

    training_data_kappa_score = round(
        cohen_kappa_score(yhat, y, weights="quadratic"), 2
    )

    training_log_loss = log_loss(y_train, train_prob_preds)
    accuracy_train = accuracy_score(y_train, train_class_preds)
    training_roc_auc = roc_auc_score(y_train, train_prob_preds)
    confusion_matrix_train = confusion_matrix(y_train, train_class_preds)

    logger.info("### Training Metrics ###")
    logger.info(f"Accuracy: {accuracy_train:.4f}")
    logger.info(f"Cohen Kappa: {training_data_kappa_score}")
    logger.info(f"ROC AUC: {training_roc_auc:.4f}")
    logger.info(f"Log Loss: {training_log_loss:.4f}")
    logger.info(f"Confusion Matrix:\n{confusion_matrix_train}")

    train_model_metrics = {
        "accuracy": accuracy_train,
        "kappa_score": training_data_kappa_score,
        "roc_auc": training_roc_auc,
        "log_loss": training_log_loss,
        "confusion_matrix": confusion_matrix_train,
    }

    return train_model_metrics


def _evaluate_testing(X_test, y_test, model) -> dict:
    test_prob_preds = model.predict_proba(X_test)[:, 1]
    test_class_preds = model.predict(X_test)

    y = np.array(y_test)
    y = y.astype(int)
    yhat = np.array(test_class_preds)
    yhat = np.clip(np.round(yhat), np.min(y), np.max(y)).astype(int)

    test_data_kappa_score = round(cohen_kappa_score(yhat, y, weights="quadratic"), 2)
    accuracy_test = accuracy_score(y_test, test_class_preds)

    fpr, tpr, _ = roc_curve(y_test, test_prob_preds)
    random_fpr, random_tpr, _ = roc_curve(y_test, [0 for _ in range(len(y_test))])

    test_log_loss = log_loss(y_test, test_prob_preds)

    f1_score_value = f1_score(y_test, test_class_preds)
    precision = precision_score(y_test, test_class_preds)
    recall = recall_score(y_test, test_class_preds)

    test_roc_auc = roc_auc_score(y_test, test_prob_preds)

    logger.info("### Test Metrics ###")
    logger.info(f"Accuracy: {accuracy_test:.4f}")
    logger.info(f"Cohen Kappa: {test_data_kappa_score}")
    logger.info(f"ROC AUC: {test_roc_auc:.4f}")
    logger.info(f"Log Loss: {test_log_loss:.4f}")
    logger.info(f"F1 Score: {f1_score_value:.4f}")
    logger.info(f"Precision: {precision:.4f}")
    logger.info(f"Recall: {recall:.4f}")

    test_model_metrics = {
        "accuracy": accuracy_test,
        "kappa_score": test_data_kappa_score,
        "roc_auc": test_roc_auc,
        "log_loss": test_log_loss,
        "f1_score": f1_score_value,
        "precision": precision,
        "recall": recall,
        "confusion_matrix": confusion_matrix(y_test, test_class_preds),
        "roc_curve": {
            "fpr": fpr,
            "tpr": tpr,
            "random_fpr": random_fpr,
            "random_tpr": random_tpr,
        },
    }

    return test_model_metrics
