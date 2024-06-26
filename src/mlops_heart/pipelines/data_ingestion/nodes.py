"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 0.19.5
"""

"""
This is a boilerplate pipeline 'data_ingestion'
generated using Kedro 0.19.5
"""

import logging
from typing import Any, Dict
import numpy as np
import pandas as pd

from great_expectations.core import ExpectationSuite, ExpectationConfiguration

from pathlib import Path

from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings

conf_path = str(Path('') / settings.CONF_SOURCE)
conf_loader = OmegaConfigLoader(conf_source=conf_path)
credentials = conf_loader["credentials"]

logger = logging.getLogger(__name__)

def make_expectation_suite(expectation_suite_name: str, feature_group: str) -> ExpectationSuite:

    expectation_suite_heart_data = ExpectationSuite(
    expectation_suite_name = expectation_suite_name)


    for i in ['age', 'sex', 'chest_pain_type', 'resting_bp_s', 'cholesterol', 'fasting_blood_sugar', 'resting_ecg', 'max_heart_rate', 'exercise_angina', 'st_slope', 'target']:
        expectation_suite_heart_data.add_expectation(
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_of_type",
                kwargs={
                    "column": i,
                    "type_": "int64",
                },
            )
        )

        #oldpeak is a float
        expectation_suite_heart_data.add_expectation(
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_of_type",
                kwargs={
                    "column": "oldpeak",
                    "type_": "float64",
                },
            )
        )

    return expectation_suite_heart_data

import hopsworks

def to_feature_store(
        data: pd.DataFrame,
        group_name: str,
        feature_group_version: int,
        description: str,
        group_description: dict,
        validation_expectation_suite: ExpectationSuite,
        credentials_input: dict
    ):

    # Connect to the feature store
    project = hopsworks.login(
        api_key_value=credentials_input["FS_API_KEY"],
        project=credentials_input["FS_PROJECT_NAME"],
    )

    feature_store = project.get_feature_store()

    # Create a feature group
    feature_group = feature_store.create_feature_group(
        name=group_name,
        version=feature_group_version,
        description=description,
        primary_key=["id"],
        online_enabled=False,
        expectation_suite = validation_expectation_suite,
    )

    #Upload data
    feature_group.insert(
        features=data,
        overwrite=False,
        write_options={
            "wait_for_job": True,
        },
    )

    # Add feature descriptions.

    for description in group_description:
        object_feature_group.update_feature_description(
            description["name"], description["description"]
        )

    # Update statistics.
    feature_group.statistics_config = {
        "enabled": True,
        "histograms": True,
        "correlations": True,
    }
    feature_group.update_statistics_config()
    feature_group.compute_statistics()

    return feature_group

def ingestion(
    data: pd.DataFrame,
    parameters: Dict[str, Any]
) -> pd.DataFrame:
    """
    Ingest the given DataFrame into the feature store after performing necessary validation and processing.

    Args:
        data (pd.DataFrame): The DataFrame to be ingested.
        parameters (Dict[str, Any]): Parameters including target column and whether to store to feature store.

    Returns:
        pd.DataFrame: The processed DataFrame ready for further use.
    """
    
    # Log initial information about the dataset
    logger.info(f"Initial dataset contains {len(data)} rows and {len(data.columns)} columns.")
    
    # Validate columns
    expected_columns = ['age', 'sex', 'chest_pain_type', 'resting_bp_s', 'cholesterol', 
                        'fasting_blood_sugar', 'resting_ecg', 'max_heart_rate', 'exercise_angina', 
                        'st_slope', 'target', 'oldpeak']
    
    missing_columns = [col for col in expected_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Data is missing the following columns: {missing_columns}")

    # Add a primary key if not present
    if 'id' not in data.columns:
        data = data.reset_index().rename(columns={"index": "id"})

    # Create expectation suites
    expectation_suite = make_expectation_suite("heart_data_expectations", "heart_data_features")
    
    # Placeholder for feature descriptions (modify as per your requirements)
    feature_descriptions = [
        {"name": col, "description": f"Description of {col}"} for col in data.columns
    ]

    # Store to feature store if required
    if parameters.get("to_feature_store", False):
        feature_store_object = to_feature_store(
            data=data,
            group_name="heart_data_features",
            feature_group_version=1,
            description="Heart data features",
            group_description=feature_descriptions,
            validation_expectation_suite=expectation_suite,
            credentials_input=credentials["feature_store"]
        )
        
        logger.info(f"Data successfully stored to feature store with feature group: {feature_store_object}")

    logger.info("Ingestion process completed.")
    return data
                