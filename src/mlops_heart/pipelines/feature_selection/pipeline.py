from kedro.pipeline import Pipeline, node
from .nodes import feature_selection
 
def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=feature_selection,
                inputs=["X_train", "y_train", "parameters"],
                outputs="best_columns",
                name="model_feature_selection",
            ),
        ]
    )