import pickle
from pathlib import Path

import numpy as np
# import pandas as pd
import sklearn

MODEL_PATH = Path(__file__).parent / 'model.pkl'


def preprocess(df, minutes=30, n_historical_cols=2):
    # TODO: type checking
    # timestamp should be int
    # measure should be int

    # convert datetime to into - shouldn't be necessary in production
    df['timestamp'] = df['timestamp'].astype(np.int64) // 10**9

    for x in range(1, n_historical_cols+1):
        df[['prev_meas', 'prev_time']] = (
            df[['measurement', 'timestamp']].shift(x)
        )
        df[f'prev_trend_{x}'] = (
            df['prev_meas'].divide(df['timestamp'] - df['prev_time'])
        )
        df = df.drop(columns=['prev_meas', 'prev_time'])

    # TODO: Other features?
    # * hour of day
    # * day of week

    # remove nans
    og_len = len(df)
    df = df.loc[~df[f'prev_trend_{n_historical_cols}'].isna()]
    n_dropped = og_len - len(df)
    assert n_dropped <= n_historical_cols

    return df


def make_prediction(user_df, model, minutes=30):
    df = preprocess(user_df, minutes)

    # TODO: add rows to predict future timestamps
    # max_time = df['timestamp'].max()
    # future_times = range(max_time, max_time + minutes * 60, 5 * 60)
    # df = df.append() ...
    predictions = model.predict(df)
    
    df = df[['timestamp']].assign(predicted_value = list(predictions))
    df['timestamp'] = df['timestamp'] + 60 * minutes

    return df
