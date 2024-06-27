from kedro.pipeline import Pipeline, node, pipeline

from .nodes import data_drift

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func= data_drift,
                inputs=["use_data","test_data"],
                outputs= "drift_result",
                name="data_drift",
            ),

        ]
    )
