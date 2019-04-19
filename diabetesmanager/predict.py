import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn


def type_check(df):
    for col in ['timestamp', 'value', 'below_threshold']:
        assert pd.api.types.is_numeric_dtype(df[col])
    
    return None


def feature_engineer(df, minutes=30, n_historical_cols=2):
    """Adds most recent CGM rates as columns"""
    type_check(df)
    
    for x in range(1, n_historical_cols+1):
        df[['prev_val', 'prev_time']] = df[['value', 'timestamp']].shift(x)
        df[f'prev_trend_{x}'] = (
            df['prev_val'].divide(df['timestamp'] - df['prev_time']))
        df = df.drop(columns=['prev_val', 'prev_time'])

    # remove nans
    og_len = len(df)
    df = df.loc[~df[f'prev_trend_{n_historical_cols}'].isna()]
    n_dropped = og_len - len(df)
    assert n_dropped <= n_historical_cols

    return df


def make_prediction(user_df, model, minutes=30):
    df = feature_engineer(user_df, minutes)
    df = df.iloc[-1:]
    prediction = model.predict(df)

    return pd.DataFrame({
        'timestamp': [df['timestamp'].max() + 60 * minutes],
        'predicted_value': [int(prediction[0].round())]
    })
