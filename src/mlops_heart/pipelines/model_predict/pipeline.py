from kedro.pipeline import Pipeline, node
import logging
from .nodes import model_predict

logging = logging.getLogger(__name__)

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=model_predict,
                inputs=[
                    "X_test",
                    "y_test",
                    "best_model",
                    "best_columns",
                    "params:use_feature_selection"
                ],
                outputs="predictions",
                name="predict_model_node"
            ),
        ]
    )
