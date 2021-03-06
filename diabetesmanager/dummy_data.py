from pathlib import Path
import pandas as pd
import numpy as np

DATA_DIR = Path(__file__).parents[1] / 'data'


def load_so_cgm():
    data_path = str(DATA_DIR / 'private' / 'dexcom_cgm')

    dfs = []
    for p in Path(data_path).iterdir():
        if str(p).endswith('.csv'):
            df = pd.read_csv(p)

            date_nans = df['Timestamp (YYYY-MM-DDThh:mm:ss)'].isna()
            n_date_nans = sum(date_nans)
            if n_date_nans > 9:
                raise Exception(f'More NaN Timestamp values than expected. '
                                f'Expected <= 9, found {n_date_nans}')
            df = df.loc[~date_nans]

            dfs.append(df)

    df = pd.concat(dfs)
    df['Timestamp (YYYY-MM-DDThh:mm:ss)'] = pd.to_datetime(
        df['Timestamp (YYYY-MM-DDThh:mm:ss)']
    ).astype(np.int64) // 10**9
    df = df.sort_values('Timestamp (YYYY-MM-DDThh:mm:ss)')

    df = df[df['Event Type'] == 'EGV']
    df['below_threshold'] = False
    df.loc[df['Glucose Value (mg/dL)'] == 'Low', 
           'below_threshold'] = True
    df.loc[df['below_threshold'], 'Glucose Value (mg/dL)'] = 39
    df['Glucose Value (mg/dL)'] = df['Glucose Value (mg/dL)'].astype(int)

    rename_dict = {
        'Timestamp (YYYY-MM-DDThh:mm:ss)': 'timestamp',
        'Glucose Value (mg/dL)': 'value',
    }

    df = df.rename(columns=rename_dict)

    df = df.groupby('timestamp').mean().reset_index()
    df['below_threshold'] = df['below_threshold'].round().astype(int)

    return df[list(rename_dict.values()) + ['below_threshold']]
