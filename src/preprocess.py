import pandas as pd
import sys
import os

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import *

def create_lag_window(df, num_lags=3, delay=1):
    """
    Adds lag and rolling window columns to the input dataframe.
    
    Parameters:
        df (pandas.DataFrame): input dataframe
        num_lags (int): number of lagged columns to create (default: 3)
        delay (int): time delay for lagged columns (default: 1)
        
    Returns:
        pandas.DataFrame: dataframe with added lag and rolling window columns
    """
    # Set the time column as the index
    df.set_index("time", inplace=True)
    df = remove_id_column(df)

    for column in df:
        for lag in range(1,num_lags+1):
            df[column + '_lag' + str(lag)] = df[column].shift(lag*-1-(delay-1))
            df[column + '_avg_window_length' + str(lag+1)] = df[column].shift(-1-(delay-1)).rolling(window=lag+1,center=False).mean().shift(1-(lag+1))

    df.dropna(inplace=True) 

    mask = (df.columns.str.contains('apparent_temperature') | df.columns.str.contains('lag') | df.columns.str.contains('window'))
    df_processed = df[df.columns[mask]]
    
    return df_processed

# Load the data into a dataframe, preprocess, split into train-test, and save
df = pd.read_csv("data/raw/train.csv")
df_processed = create_lag_window(df)
df_processed = df_processed.reset_index(drop=True)
df_train = df_processed.loc[:int(df_processed.shape[0]*0.8),:]
df_test = df_processed.loc[int(df_processed.shape[0]*0.8):,:]
df_train.to_csv("data/processed/train.csv")
df_test.to_csv("data/processed/test.csv")