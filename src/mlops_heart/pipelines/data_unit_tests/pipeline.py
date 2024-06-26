from kedro.pipeline import Pipeline, node
from .nodes import validate_data

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=validate_data,
                inputs="ingested_data",
                outputs=None,
                name="validate_and_generate_report",
            ),
        ]
    )


