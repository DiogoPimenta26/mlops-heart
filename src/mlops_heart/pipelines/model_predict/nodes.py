import pandas as pd
import logging
from typing import List, Any
import pickle
from sklearn.metrics import accuracy_score

logger = logging.getLogger(__name__)

def model_predict(
    X_test: pd.DataFrame, 
    y_test: pd.Series,
    best_model: Any,
    best_columns: List[str],
    use_feature_selection: bool
    ) -> pd.DataFrame:
    
    logger.info('Starting model prediction')
    
    # Load the best model
    if isinstance(best_model, str):
        with open(best_model, 'rb') as f:
            model = pickle.load(f)
    else:
        model = best_model

    # Ensure the test data has the same columns as the training data used for model fitting
    if use_feature_selection:
        X_test = X_test[best_columns]
    else:
        # Align columns to match those used during model training
        missing_cols = set(model.feature_names_in_) - set(X_test.columns)
        for col in missing_cols:
            X_test[col] = 0  # Adding missing columns with default value of 0
        X_test = X_test[model.feature_names_in_]  # Reorder to match training data columns

    # Make predictions
    y_test_pred = model.predict(X_test)
    
    logger.info('Predictions completed')
    
    # Calculate accuracy for the predictions
    accuracy = accuracy_score(y_test, y_test_pred)
    logger.info(f'Accuracy: {accuracy:.4f}')

    # Create a DataFrame for predictions
    predictions_df = pd.DataFrame(y_test_pred, columns=["predictions"])
    
    print(accuracy)
    
    return predictions_df


