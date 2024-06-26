"""
This is a boilerplate pipeline 'feature_selection_pipeline'
generated using Kedro 0.19.5
"""
from kedro.pipeline import Pipeline, node, pipeline
from .nodes import feature_selection

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=feature_selection,
                inputs=["X_train", "y_train", "parameters"],
                outputs=["selected_features", "feature_importance_plot"],
                name="model_feature_selection",
            ),
        ]
    )