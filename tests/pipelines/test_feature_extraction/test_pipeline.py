import pytest
import pandas as pd
from src.mlops_heart.pipelines.test_feature_extraction.nodes import feature_extraction, align_features

def test_feature_extraction():
    # Arrange
    data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'age': ['0_40', '41_50', '51_60', '61_70', '70+'],
        'sex': [1, 0, 1, 0, 1],
        'chest_pain_type': [1, 2, 3, 4, 1],
        'resting_bp_s': [140, 130, 120, 120, 120],
        'cholesterol': ['high', 'normal', 'normal', 'high', 'borderline high'],
        'fasting_blood_sugar': [0, 0, 0, 0, 0],
        'resting_ecg': [0, 1, 2, 0, 1],
        'max_heart_rate': [172, 142, 150, 165, 118],
        'exercise_angina': [0, 0, 1, 0, 0],
        'oldpeak': [0.0, 0.0, 1.5, 0.0, 0.0],
        'st_slope': [1, 2, 3, 1, 2],
        'target': [0, 0, 0, 0, 0]
    })


    # Define your expected_output DataFrame (as shown in your previous test case)
    expected_output = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'sex': [1, 0, 1, 0, 1],
        'resting_bp_s': [140, 130, 120, 120, 120],
        'fasting_blood_sugar': [0, 0, 0, 0, 0],
        'max_heart_rate': [172, 142, 150, 165, 118],
        'exercise_angina': [0, 0, 1, 0, 0],
        'oldpeak': [0.0, 0.0, 1.5, 0.0, 0.0],
        'target': [0, 0, 0, 0, 0],
        'age_0_40': [1, 0, 0, 0, 0],
        'age_41_50': [0, 1, 0, 0, 0],
        'age_51_60': [0, 0, 1, 0, 0],
        'age_61_70': [0, 0, 0, 1, 0],
        'age_70+': [0, 0, 0, 0, 1],
        'cholesterol_borderline high': [0, 0, 0, 0, 1],
        'cholesterol_high': [1, 0, 0, 1, 0],
        'cholesterol_normal': [0, 1, 1, 0, 0],
        'chest_pain_type_1': [1, 0, 0, 0, 1],
        'chest_pain_type_2': [0, 1, 0, 0, 0],
        'chest_pain_type_3': [0, 0, 1, 0, 0],
        'chest_pain_type_4': [0, 0, 0, 1, 0],
        'resting_ecg_0': [1, 0, 0, 1, 0],
        'resting_ecg_1': [0, 1, 0, 0, 1],
        'resting_ecg_2': [0, 0, 1, 0, 0],
        'st_slope_1': [1, 0, 0, 1, 0],
        'st_slope_2': [0, 1, 0, 0, 1],
        'st_slope_3': [0, 0, 1, 0, 0]
    })

    # Act
    result = feature_extraction(data)
    
    # Debugging output to inspect result and expected_output
    print("Columns generated in result:", result.columns)
    print("Columns in expected_output:", expected_output.columns)

    # Assert
    assert sorted(result.columns) == sorted(expected_output.columns), \
        f"Column names mismatch. Result columns: {result.columns}, Expected columns: {expected_output.columns}"

    # Additional assertion to check DataFrame equality
    pd.testing.assert_frame_equal(result, expected_output)
