import pandas as pd
import logging
from typing import Dict, Any, List
import numpy as np
import pickle
import yaml
import os
import warnings
warnings.filterwarnings("ignore", category=Warning)
import mlflow
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import shap
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)

def model_train(
    X_train: pd.DataFrame, 
    X_test: pd.DataFrame, 
    y_train: pd.DataFrame, 
    y_test: pd.DataFrame,
    parameters: Dict[str, Any], 
    best_columns: List[str]
) -> List[Any]:

    # Initialize results dictionary
    results_dict = {}

    # Enable autologging
    with open('conf/local/mlflow.yml') as f:
        experiment_name = yaml.load(f, Loader=yaml.loader.SafeLoader)['tracking']['experiment']['name']
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
    logger.info('Starting first step of model selection: Comparing between modes types')
    mlflow.sklearn.autolog(log_model_signatures=True, log_input_examples=True)

    # Loop over models to train
    for model_type in parameters["models_to_train"]:
        with mlflow.start_run(experiment_id=experiment_id, nested=True):
            try:
                if model_type == "random_forest":
                    classifier = RandomForestClassifier(**parameters['rf_params'])
                elif model_type == "decision_tree":
                    classifier = DecisionTreeClassifier(**parameters['decision_tree_params'])
                else:
                    raise ValueError(f"Unsupported model type: {model_type}")

                if parameters["use_feature_selection"]:
                    logger.info(f"Using feature selection in model train...")
                    X_train_model = X_train[best_columns]
                    X_test_model = X_test[best_columns]
                else:
                    X_train_model = X_train
                    X_test_model = X_test

                y_train_model = np.ravel(y_train)
                model = classifier.fit(X_train_model, y_train_model)

                # Making predictions
                y_train_pred = model.predict(X_train_model)
                y_test_pred = model.predict(X_test_model)

                # Evaluating model
                acc_train = accuracy_score(y_train_model, y_train_pred)
                acc_test = accuracy_score(y_test, y_test_pred)

                # Saving results in dict
                results_dict[model_type] = {
                    'classifier': classifier.__class__.__name__,
                    'train_score': acc_train,
                    'test_score': acc_test
                }

                # Logging in MLflow
                run_id = mlflow.last_active_run().info.run_id
                logger.info(f"Logged train model in run {run_id}")
                logger.info(f"Accuracy for {model_type} is {acc_test}")

                # Register the model in MLflow
                mlflow.sklearn.log_model(model, f"{model_type}_model")
                model_uri = f"runs:/{run_id}/{model_type}_model"
                logger.info(f"Registered model: {model_uri}")

                # Optionally, you can set tags and create aliases for the model
                mlflow.register_model(model_uri, model_type.capitalize())
                logger.info(f"Registered model version")

            except Exception as ex:
                logger.error(f"Failed to train {model_type} model: {ex}")
                raise

    # Convert the dictionary to a list in the order of your node's output definition
    output_list = [
        results_dict.get("random_forest", {}).get("classifier", None),
        results_dict.get("decision_tree", {}).get("classifier", None),
        results_dict.get("random_forest", {}).get("train_score", None),
        results_dict.get("decision_tree", {}).get("train_score", None),
        results_dict.get("random_forest", {}).get("test_score", None),
        results_dict.get("decision_tree", {}).get("test_score", None)
    ]

    return output_list
