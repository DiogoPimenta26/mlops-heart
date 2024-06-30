import logging
from kedro.pipeline import Pipeline, node

from .nodes import model_predict

logger = logging.getLogger(__name__)

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                model_predict,
                inputs=["best_model", "best_columns","X_test", "y_test"],
                outputs=None,
            ),
        ]
    )