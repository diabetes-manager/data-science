import re
import xml.etree.cElementTree as ET
from pathlib import Path

import pandas as pd
# from dotenv import load_dotenv

# load_dotenv()

DATA_DIR = Path(__file__).parents[1] / 'data'

def load_uci():
    """Load data from http://archive.ics.uci.edu/ml/datasets/diabetes"""
    data_path = str(DATA_DIR / 'public' / 'uci')
    dfs = []
    for p in Path(data_path).iterdir():
        match = re.search(r'\d\d$', str(p))
        if match:
            df = pd.read_csv(p, sep='\t', header=None, 
                             names=['Date', 'Time', 'Code', 'Value'])
            df['person_id'] = int(match[0])
            dfs.append(df)
    df = pd.concat(dfs)

    code_map = {
        33: 'Regular insulin dose',
        34: 'NPH insulin dose',
        35: 'UltraLente insulin dose',
        48: 'Unspecified blood glucose measurement',
        57: 'Unspecified blood glucose measurement',
        58: 'Pre-breakfast blood glucose measurement',
        59: 'Post-breakfast blood glucose measurement',
        60: 'Pre-lunch blood glucose measurement',
        61: 'Post-lunch blood glucose measurement',
        62: 'Pre-supper blood glucose measurement',
        63: 'Post-supper blood glucose measurement',
        64: 'Pre-snack blood glucose measurement',
        65: 'Hypoglycemic symptoms',
        66: 'Typical meal ingestion',
        67: 'More-than-usual meal ingestion',
        68: 'Less-than-usual meal ingestion',
        69: 'Typical exercise activity',
        70: 'More-than-usual exercise activity',
        71: 'Less-than-usual exercise activity',
        72: 'Unspecified special event',
    }
    
    df['code_cat'] = df['Code'].map(code_map)
    
    df['date_time'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], 
                                     format="%m-%d-%Y %H:%M", errors='coerce')
    
    df = df.drop(columns=['Date', 'Time'])
    
    print(f"{sum(df['date_time'].isna())} records failed to convert to date")
    df = df.loc[~df['date_time'].isna()]
    
    # drop entries entered at 8AM, 12AM, 4PM, 10PM
    mask = (df['date_time'].dt.hour.isin([8, 12, 18, 22]) & 
            (df['date_time'].dt.minute == 0))
    df = df.loc[~mask]

    return df


def load_tidepool_dummy():
    """Assumed fake data from https://github.com/tidepool-org
    Could be a useful data structure to emulate"""
    data_path = ('https://raw.githubusercontent.com/tidepool-org/'
                 'data-analytics/master/examples/example-data/'
                 'example-from-j-jellyfish.csv')

    return pd.read_csv(data_path)


def load_so_pump():
    data_path = str(DATA_DIR / 'private' / 'omnipod_pump' / 
                    'omnipod_export_2019-04-13.XML')
    tree = ET.parse(data_path)
    root = tree.getroot()
    
    list_dicts = []
    for record in root:
        list_dicts.append(record[0].attrib)
        
    return pd.DataFrame(list_dicts)


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

    return pd.concat(dfs)
