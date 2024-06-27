"""
This is a boilerplate pipeline 'data_split'
generated using Kedro 0.19.5
"""

import pandas as pd

#split the data randomly for the unit tests
def split_random(data: pd.DataFrame):

    use_data = data.sample(frac=0.8,random_state=200)
    test_data = data.drop(use_data.index)

    return use_data, test_data

