"""
This is a boilerplate pipeline 'model_tunning'
generated using Kedro 0.19.5
"""
import logging
import pandas as pd
import numpy as np
import mlflow
import yaml
from typing import Dict, Any
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
 
logger = logging.getLogger(__name__)
 
def hyperparameter_tuning(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.DataFrame,
    y_test: pd.DataFrame,
    champion_model: Dict[str, Any],
    parameters: Dict[str, Any],
    best_columns: List[str]
) -> Dict[str, Any]:
 
    model_type = champion_model['classifier']
    if model_type == "RandomForestClassifier":
        classifier = RandomForestClassifier()
        param_grid = parameters['rf_param_grid']
    elif model_type == "DecisionTreeClassifier":
        classifier = DecisionTreeClassifier()
        param_grid = parameters['decision_tree_param_grid']
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
 
    if parameters["use_feature_selection"]:
        X_train_model = X_train[best_columns]
        X_test_model = X_test[best_columns]
    else:
        X_train_model = X_train
        X_test_model = X_test
 
    y_train_model = np.ravel(y_train)
 
    search = GridSearchCV(classifier, param_grid, cv=parameters['cv'], scoring='accuracy', n_jobs=-1)
    search.fit(X_train_model, y_train_model)
 
    best_model = search.best_estimator_
    best_params = search.best_params_
 
    y_train_pred = best_model.predict(X_train_model)
    y_test_pred = best_model.predict(X_test_model)
    acc_train = accuracy_score(y_train_model, y_train_pred)
    acc_test = accuracy_score(y_test, y_test_pred)
 
    with open('conf/local/mlflow.yml') as f:
        experiment_name = yaml.load(f, Loader=yaml.loader.SafeLoader)['tracking']['experiment']['name']
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
 
    with mlflow.start_run(experiment_id=experiment_id, nested=True):
        mlflow.sklearn.log_model(best_model, f"{model_type}_tuned_model")
        mlflow.log_params(best_params)
        mlflow.log_metric("train_accuracy", acc_train)
        mlflow.log_metric("test_accuracy", acc_test)
 
    return {
        'best_model': best_model,
        'best_params': best_params,
        'train_accuracy': acc_train,
        'test_accuracy': acc_test
    }