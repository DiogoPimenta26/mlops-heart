import seaborn
import pandas as pd
import nannyml as nml
import numpy as np
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def data_drift(data_reference: pd.DataFrame, data_analysis: pd.DataFrame):
    
    constant_threshold = nml.thresholds.ConstantThreshold(lower=0.1, upper=0.5)
    data_analysis = data_analysis[data_analysis['cholesterol'] > 240]

    # Let's initialize the object that will perform the Univariate Drift calculations for the columns that have the potential to change over time 
    univariate_calculator = nml.UnivariateDriftCalculator(
    column_names=['cholesterol', 'age', 'max_heart_rate', 'resting_bp_s'],
    chunk_size= 10,
    timestamp_column_name=None,
    categorical_methods=['jensen_shannon'],
    thresholds={"jensen_shannon":constant_threshold},
    )

    univariate_calculator.fit(data_reference)
    results = univariate_calculator.calculate(data_analysis).filter(period='analysis', column_names=['cholesterol', 'age', 'max_heart_rate', 'resting_bp_s']).to_df()
    
    figure = univariate_calculator.calculate(data_analysis).filter(period='analysis', column_names=['cholesterol', 'age', 'max_heart_rate', 'resting_bp_s']).plot(kind='drift')
    figure.write_html("data/08_reporting/univariate_nml.html")

    #Generate the report using the same method jensen-shannon and using evidently
    data_drift_report = Report(metrics=[DataDriftPreset(num_stattest='jensenshannon')])

    data_drift_report.run(current_data=data_analysis[['cholesterol', 'age', 'max_heart_rate', 'resting_bp_s']] , reference_data=data_reference[['cholesterol', 'age', 'max_heart_rate', 'resting_bp_s']], column_mapping=None)
    data_drift_report.save_html("data/08_reporting/data_drift_report.html")

    return results
