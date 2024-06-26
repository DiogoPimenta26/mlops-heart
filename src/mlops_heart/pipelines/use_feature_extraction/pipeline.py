"""
This is a boilerplate pipeline 'feature_extraction'
generated using Kedro 0.19.5
"""
from kedro.pipeline import Pipeline, node
from .nodes import feature_extraction, align_features

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=feature_extraction,
                inputs="use_preprocessed_data",
                outputs="use_features",
                name="use_extract_features_node",
            ),
            node(
                func=align_features,
                inputs=["use_features", "params:feature_columns"],
                outputs="use_aligned_features",
                name="use_align_features_node",
            )
        ]
    )