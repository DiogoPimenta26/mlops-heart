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
                inputs="test_preprocessed_data",
                outputs="test_features",
                name="test_extract_features_node",
            ),
            node(
                func=align_features,
                inputs=["test_features", "params:feature_columns"],
                outputs="test_aligned_features",
                name="test_align_features_node",
            )
        ]
    )