from kedro.pipeline import Pipeline, node

from .nodes import model_tune

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=model_tune,
                inputs=[
                    "X_train",
                    "X_test",
                    "y_train",
                    "y_test",
                    "champion_model_output",
                    "params:tuning_params",
                    "best_columns"
                ],
                outputs=[
                    "best_model",
                    "best_params",
                ],
                name="tune_model_node"
            ),
        ]
    )
