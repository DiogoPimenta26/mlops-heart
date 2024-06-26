"""
This is a boilerplate pipeline 'test_data_preprocessing'
generated using Kedro 0.19.5
"""

from kedro.pipeline import Pipeline, node
from .nodes import remove_duplicates, remove_zero_bp, remove_zero_cholesterol, max_heart_rate_outliers, bin_age, bin_cholesterol, remove_zero_st_slope

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=remove_duplicates,
                inputs="test_data",
                outputs="test_output_dataframe_after_duplicates_removal",
                name="test_remove_duplicates_node"
            ),
            node(
                func=remove_zero_bp,
                inputs="test_output_dataframe_after_duplicates_removal",
                outputs="test_output_dataframe_after_zero_bp_removal",
                name="test_remove_zero_bp_node"
            ),
            node(
                func=remove_zero_cholesterol,
                inputs="test_output_dataframe_after_zero_bp_removal",
                outputs="test_output_dataframe_after_zero_cholesterol_removal",
                name="test_remove_zero_cholesterol_node"
            ),
            node(
                func=remove_zero_st_slope,
                inputs="test_output_dataframe_after_zero_cholesterol_removal",
                outputs="test_output_dataframe_after_zero_st_slope_removal",
                name="test_remove_zero_st_slope_node"
            ),
            node(
                func=max_heart_rate_outliers,
                inputs="test_output_dataframe_after_zero_cholesterol_removal",
                outputs="test_output_dataframe_after_max_hr_outliers_removal",
                name="test_max_heart_rate_outliers_node"
            ),
            node(
                func=bin_age,
                inputs="test_output_dataframe_after_max_hr_outliers_removal",
                outputs="test_output_dataframe_after_age_binning",
                name="test_bin_age_node"
            ),
            node(
                func=bin_cholesterol,
                inputs="test_output_dataframe_after_age_binning",
                outputs="test_preprocessed_data",
                name="test_bin_cholesterol_node"
            ),
        ]
    )