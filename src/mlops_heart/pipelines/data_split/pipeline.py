"""
This is a boilerplate pipeline 'data_split'
generated using Kedro 0.19.5
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import split_random


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
    [
        node(
            func = split_random,
            inputs = 'ingested_data',
            outputs = ['use_data', 'test_data'],
            name = "Split_data_for_unit_tests"
        )
    ])
