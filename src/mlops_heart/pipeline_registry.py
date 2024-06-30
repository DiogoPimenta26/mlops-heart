"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from mlops_heart.pipelines import (
    data_ingestion as di,
    data_split as ds,
    data_unit_tests as dut,
    use_data_preprocessing as udp,
    use_feature_extraction as ufe,
    test_data_preprocessing as tdp,
    test_feature_extraction as tfe,
    train_test_split as tts,
    feature_selection as fs,
    model_train as mt,
    model_tunning as mtu,
    model_predict as mp,
    #data_drift as dd,
)


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
   

    data_ingestion_pipeline = di.create_pipeline()
    data_split_pipeline = ds.create_pipeline()
    data_unit_tests_pipeline = dut.create_pipeline()
    use_data_preprocessing_pipeline = udp.create_pipeline()
    use_feature_extraction_pipeline = ufe.create_pipeline()
    test_data_preprocessing_pipeline = tdp.create_pipeline()
    test_feature_extraction_pipeline = tfe.create_pipeline()
    train_test_split_pipeline = tts.create_pipeline()
    feature_selection_pipeline = fs.create_pipeline()
    model_train_pipeline = mt.create_pipeline()
    model_tunning_pipeline = mtu.create_pipeline()
    model_predict_pipeline = mp.create_pipeline()
#    data_drift_pipeline = dd.create_pipeline()

    return {
        "__default__": data_ingestion_pipeline,
        "data_ingestion": data_ingestion_pipeline,
        "data_split": data_split_pipeline,
        "data_unit_tests": data_unit_tests_pipeline,
        "use_data_preprocessing": use_data_preprocessing_pipeline,
        "use_feature_extraction": use_feature_extraction_pipeline,
        "test_data_preprocessing": test_data_preprocessing_pipeline,
        "test_feature_extraction": test_feature_extraction_pipeline,
        "train_test_split": train_test_split_pipeline,
        "feature_selection": feature_selection_pipeline,
        "model_train": model_train_pipeline,
        "model_tunning": model_tunning_pipeline,
        "model_predict": model_predict_pipeline,
 #       "data_drift": data_drift_pipeline,
    }