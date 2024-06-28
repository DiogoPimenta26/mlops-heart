from kedro.pipeline import Pipeline, node

from .nodes import model_train

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                model_train,
                inputs=["X_train", "X_test", "y_train", "y_test", "parameters", "best_columns"],
                outputs=[
                    "production_model_RF",
                    "production_model_dt",
                    "production_columns_RF",
                    "production_columns_dt",
                    "production_model_metrics_rf",
                    "production_model_metrics_dt",
                ],
            ),
        ]
    )
