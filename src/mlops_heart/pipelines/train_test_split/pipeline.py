"""
This is a boilerplate pipeline 'train_test_split'
generated using Kedro 0.19.5
"""
from kedro.pipeline import Pipeline, node
from .nodes import split_data

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=split_data,
            inputs=dict(data="use_aligned_features", test_size="params:train_test_split.test_size", random_state="params:train_test_split.random_state"),
            outputs=["X_train", "X_test", "y_train", "y_test"],
            name="split_data_node"
        )
    ])