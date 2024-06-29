"""
This is a boilerplate pipeline 'model_tunning'
generated using Kedro 0.19.5
"""

from kedro.pipeline import Pipeline, pipeline

from kedro.pipeline import Pipeline, node
from .nodes import hyperparameter_tuning
 
def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                hyperparameter_tuning,
                inputs=["X_train", "X_test", "y_train", "y_test", "champion_model_output", "parameters", "best_columns"],
                outputs="tuned_model_results",
                name="hyperparameter_tuning_node"
            ),
        ]
    )

