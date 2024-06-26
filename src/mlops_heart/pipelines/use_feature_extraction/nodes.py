"""
This is a boilerplate pipeline 'feature_extraction'
generated using Kedro 0.19.5
"""
import pandas as pd

def feature_extraction(data: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts features from the input data.

    Args:
        data: Input data.

    Returns:
        Extracted features.
    """
    # One-hot encoding age
    data = pd.get_dummies(data, columns=["age"], dtype="int64")
    
    # One-hot encoding cholesterol
    data = pd.get_dummies(data, columns=["cholesterol"], dtype="int64")
    
    # One-hot encoding chest pain type
    data = pd.get_dummies(data, columns=["chest_pain_type"], dtype="int64")
    
    # One-hot encoding resting ecg
    data = pd.get_dummies(data, columns=["resting_ecg"], dtype="int64")
    
    # One-hot encoding ST slope
    data = pd.get_dummies(data, columns=["st_slope"], dtype="int64")
    
    return data


def align_features(data: pd.DataFrame, feature_columns: list) -> pd.DataFrame:
    """
    Aligns the features in the input data.

    Args:
        data: Input data.
        feature_columns: List of feature columns.

    Returns:
        Aligned features.
    """
    # Align the features
    data = data[feature_columns]
    
    # if lenght of feature_columns is not equal to the number of columns in data raise an error
    if len(feature_columns) != data.shape[1]:
        raise ValueError('Mismatch in feature columns')
    
    else:
        print('Features are matched')
    
    return data