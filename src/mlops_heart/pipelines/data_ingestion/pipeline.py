"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 0.19.5
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import ingestion


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
    [
        node(
            func = ingestion,
            inputs= ['heart_data_raw','parameters'],
            outputs= 'ingested_data',
            name= 'ingestion'
        )
    ])
