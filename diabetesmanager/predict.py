import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn


def preprocess(df, minutes=30, n_historical_cols=2):
    # TODO: type checking
    # timestamp should be int
    # measure should be int

    # convert datetime to into - shouldn't be necessary in production
    df['timestamp'] = df['timestamp'].astype(np.int64) // 10**9

    for x in range(1, n_historical_cols + 1):
        df[['prev_meas', 'prev_time']] = (df[['value', 'timestamp']].shift(x))
        df[f'prev_trend_{x}'] = (
            df['prev_meas'].divide(df['timestamp'] - df['prev_time']))
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
    df = df.iloc[-1:]
    predictions = model.predict(df)

    return pd.DataFrame({
        'timestamp': [df['timestamp'].max() + 60 * minutes],
        'predicted_value': [int(predictions[0].round())]
    })
