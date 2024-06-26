"""
This is a boilerplate pipeline 'train_test_split'
generated using Kedro 0.19.5
"""
"""
This is a boilerplate pipeline 'train_test_split'
generated using Kedro 0.19.5
"""
import pandas as pd
from sklearn.model_selection import train_test_split

def split_data(data: pd.DataFrame, test_size: float, random_state: int) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    X = data.drop(columns=['target'])
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test