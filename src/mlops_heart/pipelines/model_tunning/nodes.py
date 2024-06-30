import pandas as pd
import logging
from typing import Dict, Any, List
import numpy as np
import mlflow
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import yaml

logger = logging.getLogger(__name__)

def model_tune(
    X_train: pd.DataFrame, 
    X_test: pd.DataFrame, 
    y_train: pd.DataFrame, 
    y_test: pd.DataFrame,
    champion_model_output: List[Any],
    tuning_params: Dict[str, Any],
    best_columns: List[str]
    ) -> Dict[str, Any]:

    # Extracting the champion model information
    champion_model_name, _, _ = champion_model_output

    # Select the model class based on the champion model name
    if champion_model_name == "RandomForestClassifier":
        from sklearn.ensemble import RandomForestClassifier
        model_class = RandomForestClassifier
    elif champion_model_name == "DecisionTreeClassifier":
        from sklearn.tree import DecisionTreeClassifier
        model_class = DecisionTreeClassifier
    else:
        raise ValueError(f"Unsupported model type: {champion_model_name}")

    # Initialize the model
    model = model_class()

    # Perform feature selection if needed
    if tuning_params["use_feature_selection"]:
        X_train_model = X_train[best_columns]
        X_test_model = X_test[best_columns]
    else:
        X_train_model = X_train
        X_test_model = X_test

    y_train_model = np.ravel(y_train)

    # Initialize GridSearchCV
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=tuning_params["param_grid"],
        cv=tuning_params.get("cv", 5),
        scoring=tuning_params.get("scoring", "accuracy"),
        n_jobs=tuning_params.get("n_jobs", -1)
    )

    # Enable autologging
    with open('conf/local/mlflow.yml') as f:
        experiment_name = yaml.load(f, Loader=yaml.loader.SafeLoader)['tracking']['experiment']['name']
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
    mlflow.sklearn.autolog(log_model_signatures=True, log_input_examples=True)

    # Perform the grid search within an MLflow run
    with mlflow.start_run(experiment_id=experiment_id, nested=True) as run:
        grid_search.fit(X_train_model, y_train_model)

        # Extracting the best model and its performance
        best_model = grid_search.best_estimator_
        best_params = grid_search.best_params_
        best_score = grid_search.best_score_

        # Making predictions on the test set
        y_test_pred = best_model.predict(X_test_model)
        test_score = accuracy_score(y_test, y_test_pred)

        # Logging the best model and parameters
        mlflow.sklearn.log_model(best_model, f"best_{champion_model_name}_model")
        mlflow.log_params(best_params)
        mlflow.log_metric("test_accuracy", test_score)

        # Register the best model in MLflow
        run_id = mlflow.active_run().info.run_id
        model_uri = f"runs:/{run_id}/best_{champion_model_name}_model"
        mlflow.register_model(model_uri, f"Best{champion_model_name}")

        print(f"Best model: {best_model}")
        print(f"Best parameters: {best_params}")
        print(f"Best score: {best_score}")
        print(f"Test score: {test_score}")
    


    return best_model, best_params

    

