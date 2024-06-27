import pandas as pd
import great_expectations as ge
import logging
import json

def validate_data(data: pd.DataFrame) -> pd.DataFrame:
    # Convert the pandas DataFrame to a Great Expectations DataFrame
    pd_df_ge = ge.from_pandas(data)

    # Define the expected number of columns
    assert pd_df_ge.expect_table_column_count_to_equal(13).success, "Column count does not match expected value"

    # Define the columns to check for existence
    expected_columns = [
        'id', 'age', 'sex', 'chest_pain_type', 'resting_bp_s', 'cholesterol',
        'fasting_blood_sugar', 'resting_ecg', 'max_heart_rate', 'exercise_angina',
        'oldpeak', 'st_slope', 'target'
    ]

    # Check if each expected column exists
    for column in expected_columns:
        assert pd_df_ge.expect_column_to_exist(column).success, f"Column {column} does not exist"

    # Define expected data types for each column
    expected_types = {
        'age': 'int64',
        'sex': 'int64',
        'chest_pain_type': 'int64',
        'resting_bp_s': 'int64',
        'cholesterol': 'int64',
        'fasting_blood_sugar': 'int64',
        'resting_ecg': 'int64',
        'max_heart_rate': 'int64',
        'exercise_angina': 'int64',
        'oldpeak': 'float64',
        'st_slope': 'int64',
        'target': 'int64'
    }

    # Check the data type of each column
    for column, expected_type in expected_types.items():
        assert pd_df_ge.expect_column_values_to_be_of_type(column, expected_type).success, f"{column} is not of type {expected_type}"

#TODO AQUI POR AS COLUNAS MAIS IMPORTANTES DO FEATURE SELECTION
    # Check for missing values in critical columns
    critical_columns = ['age', 'sex', 'chest_pain_type', 'resting_bp_s', 'cholesterol', 'max_heart_rate', 'target']

    for column in critical_columns:
        assert pd_df_ge.expect_column_values_to_not_be_null(column).success, f"Column {column} contains null values"

    # Check that categorical columns contain only expected values
    expected_values = {
        'sex': [0, 1],
        'chest_pain_type': [1, 2, 3, 4],
        'fasting_blood_sugar': [0, 1],
        'exercise_angina': [0, 1],
        'target': [0, 1]
    }

    for column, values in expected_values.items():
        assert pd_df_ge.expect_column_values_to_be_in_set(column, values).success, f"Column {column} contains unexpected values"

    # Generate the validation report
    validation_report = pd_df_ge.validate()

    # Convert validation report to a JSON string
    validation_report_json = validation_report.to_json_dict()

    # Flatten the JSON structure and convert it to a DataFrame
    validation_report_df = pd.json_normalize(validation_report_json)

    # Additional reporting for numerical and categorical columns
    report = {'column': [], 'min': [], 'max': [], 'mean': [], 'unexpected_values': [], 'mode': []}

    for column in data.columns:
        report['column'].append(column)

        if pd.api.types.is_numeric_dtype(data[column]):
            report['min'].append(data[column].min())
            report['max'].append(data[column].max())
            report['mean'].append(data[column].mean())
            report['unexpected_values'].append(None)
            report['mode'].append(data[column].mode()[0])
        else:
            report['min'].append(None)
            report['max'].append(None)
            report['mean'].append(None)
            if column in expected_values:
                unexpected_values = set(data[column].unique()) - set(expected_values[column])
                report['unexpected_values'].append(list(unexpected_values))
            else:
                report['unexpected_values'].append(None)
            report['mode'].append(data[column].mode()[0])

    additional_report_df = pd.DataFrame(report)

    # Save the validation report to a CSV file
    validation_report_filepath = "data/08_reporting/validation_report.csv"
    validation_report_df.to_csv(validation_report_filepath, index=False)

    # Save the additional report to a CSV file
    additional_report_filepath = "data/08_reporting/additional_report.csv"
    additional_report_df.to_csv(additional_report_filepath, index=False)

    log = logging.getLogger(__name__)
    log.info("Data passed the unit tests")
    log.info(f"Validation report saved to {validation_report_filepath}")
    log.info(f"Additional report saved to {additional_report_filepath}")

    print("Data validation passed")

    return additional_report_df

