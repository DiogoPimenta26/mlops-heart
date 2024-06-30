from kedro.pipeline import Pipeline, node

from .nodes import model_train

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                model_train,
                inputs=["X_train", "X_test", "y_train", "y_test", "parameters", "best_columns"],
                outputs=[
                    "champion_model_output",
                    "all_models_output"
                ],
            ),
        ]
    )

