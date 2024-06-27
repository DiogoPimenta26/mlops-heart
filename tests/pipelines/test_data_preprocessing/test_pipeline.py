import pytest
import pandas as pd
from src.mlops_heart.pipelines.use_data_preprocessing import (
    remove_duplicates,
    remove_zero_bp,
    remove_zero_cholesterol,
    remove_zero_st_slope,
    max_heart_rate_outliers,
    bin_age,
    bin_cholesterol
)

def test_remove_duplicates():
    # Arrange
    data = pd.DataFrame({
        'column1': [1, 1, 2, 2, 3],
        'resting_bp_s': [120, 120, 130, 130, 140]
    })
    expected_output = pd.DataFrame({
        'column1': [1, 2, 3],
        'resting_bp_s': [120, 130, 140]
    }).reset_index(drop=True)

    # Act
    result = remove_duplicates(data).reset_index(drop=True)

    # Assert
    pd.testing.assert_frame_equal(result, expected_output)

def test_remove_zero_bp():
    # Arrange
    data = pd.DataFrame({
        'resting_bp_s': [120, 0, 130, 0, 140],
        'cholesterol': [200, 220, 250, 270, 300]
    })
    expected_output = pd.DataFrame({
        'resting_bp_s': [120, 130, 140],
        'cholesterol': [200, 250, 300]
    }).reset_index(drop=True)

    # Act
    result = remove_zero_bp(data).reset_index(drop=True)

    # Assert
    pd.testing.assert_frame_equal(result, expected_output)

def test_remove_zero_cholesterol():
    # Arrange
    data = pd.DataFrame({
        'cholesterol': [200, 0, 250, 0, 300],
        'resting_bp_s': [120, 130, 140, 150, 160]
    })
    expected_output = pd.DataFrame({
        'cholesterol': [200, 250, 300],
        'resting_bp_s': [120, 140, 160]
    }).reset_index(drop=True)

    # Act
    result = remove_zero_cholesterol(data).reset_index(drop=True)

    # Assert
    pd.testing.assert_frame_equal(result, expected_output)

def test_remove_zero_st_slope():
    # Arrange
    data = pd.DataFrame({
        'st_slope': [1, 0, 2, 0, 3],
        'resting_bp_s': [120, 130, 140, 150, 160]
    })
    expected_output = pd.DataFrame({
        'st_slope': [1, 2, 3],
        'resting_bp_s': [120, 140, 160]
    }).reset_index(drop=True)

    # Act
    result = remove_zero_st_slope(data).reset_index(drop=True)

    # Assert
    pd.testing.assert_frame_equal(result, expected_output)

def test_max_heart_rate_outliers():
    # Arrange
    data = pd.DataFrame({
        'max_heart_rate': [71, 72, 150, 202, 203],
        'resting_bp_s': [120, 130, 140, 150, 160]
    })
    expected_output = pd.DataFrame({
        'max_heart_rate': [72, 150, 202],
        'resting_bp_s': [130, 140, 150]
    }).reset_index(drop=True)

    # Act
    result = max_heart_rate_outliers(data).reset_index(drop=True)

    # Assert
    pd.testing.assert_frame_equal(result, expected_output)

def test_bin_age():
    # Arrange
    data = pd.DataFrame({
        'age': [25, 45, 55, 65, 75, 85],
        'resting_bp_s': [120, 130, 140, 150, 160, 170]
    })
    expected_output = pd.DataFrame({
        'age': ['0-40', '41-50', '51-60', '61-70', '71-80', '81-90'],
        'resting_bp_s': [120, 130, 140, 150, 160, 170]
    }).reset_index(drop=True)

    # Act
    result = bin_age(data).reset_index(drop=True)

    # Assert
    pd.testing.assert_frame_equal(result, expected_output)

def test_bin_cholesterol():
    # Arrange
    data = pd.DataFrame({
        'cholesterol': [180, 210, 260],
        'resting_bp_s': [120, 130, 140]
    })
    expected_output = pd.DataFrame({
        'cholesterol': ['normal', 'borderline high', 'high'],
        'resting_bp_s': [120, 130, 140]
    }).reset_index(drop=True)

    # Act
    result = bin_cholesterol(data).reset_index(drop=True)

    # Assert
    pd.testing.assert_frame_equal(result, expected_output)
