import pickle
from pathlib import Path

import numpy as np
# import pandas as pd
import sklearn

MODEL_PATH = Path(__file__).parent / 'model.pkl'


def preprocess(df, minutes=30, n_historical_cols=2):
    # convert datetime to int
    df['timestamp'] = df['timestamp'].astype(np.int64) // 10**9
    
    for x in range(1, n_historical_cols+1):
        df[['prev_meas', 'prev_time']] = df[['measurement', 'timestamp']].shift(x)
        df[f'prev_trend_{x}'] = (
            df['prev_meas'].divide(df['timestamp'] - df['prev_time']))
        df = df.drop(columns=['prev_meas', 'prev_time'])
    
    # get 30 minute future value
    df = append_future_value_col(df, minutes)
    
    # remove nans
    og_len = len(df)
    df = df.loc[~df[f'{minutes}_minutes'].isna() & 
                ~df[f'prev_trend_{n_historical_cols}'].isna()]
    n_dropped = og_len - len(df)
    assert n_dropped < (10 + n_historical_cols)

    return df


def append_future_value_col(df, minutes):
    seconds = minutes * 60
    
    df[f'{minutes}_minutes'] = np.interp(
        df['timestamp'].add(seconds), df['timestamp'],
        df['measurement']
    )
    
    max_valid_time = df['timestamp'].max() - seconds
    df.loc[df['timestamp'] > max_valid_time, f'{minutes}_minutes'] = np.nan

    return df


def make_prediction(user_df, model, minutes=30):
    df = preprocess(user_df, minutes)
    df = df.drop(columns=[f'{minutes}_minutes'])
    predictions = model.predict(df)
    
    df = df[['timestamp']].assign(predicted_value = list(predictions))
    df['timestamp'] = df['timestamp'] + 60 * minutes
    
    return df
