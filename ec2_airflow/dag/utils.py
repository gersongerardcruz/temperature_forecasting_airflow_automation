import pandas as pd
import boto3
import io 
from openmeteo_py import Hourly, Options, OWmanager
from datetime import datetime
from airflow.hooks.S3_hook import S3Hook
from io import StringIO

def get_weather_data(filename, bucket_name, latitude=14.5995, longitude=120.9842, past_days=2, timezone="Asia/Shanghai"):
    """
    Retrieves weather data from OpenWeather API and returns a pandas dataframe with relevant columns.

    Args:
    - latitude: float - The latitude of the location you want to retrieve data for
    - longitude: float - The longitude of the location you want to retrieve data for
    - past_days: int - The number of days of past data you want to retrieve
    - timezone: str - The timezone of the location you want to retrieve data for

    Returns:
    - pandas dataframe - A dataframe with the relevant weather data columns
    """
    # Set up API options and download data
    hourly = Hourly()
    options = Options(latitude, longitude, past_days=past_days, timezone=timezone)
    mgr = OWmanager(options, hourly.all())
    meteo = mgr.get_data()

    # Convert to pandas dataframe
    df = pd.DataFrame(meteo['hourly'])

    # Get only data equal to or less than current time
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M')
    df = df[df["time"] <= current_time]

    # Define columns to retain for the model to predict temperature
    columns_to_keep = [
        "time",
        "apparent_temperature",
        "relativehumidity_2m",
        "dewpoint_2m",
        "pressure_msl",
        "cloudcover",
        "windspeed_10m",
        "precipitation",
        "direct_radiation",
        "soil_temperature_0cm"
    ]
    df = df[columns_to_keep]

    # Create an S3FileSystem object with the IAM role specified
    s3 = boto3.client('s3')

    bucket_name = bucket_name
    key = f"{filename}.csv"

    # Write data to a file on S3
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    s3.put_object(Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=key)

def remove_id_column(df):
    """
    Removes the ID column from a pandas dataframe.
    Takes into account different spellings of "ID" and "Unnamed: 0".
    Parameters:
        df (pandas.DataFrame): The input dataframe.
    Returns:
        pandas.DataFrame: The dataframe with the ID column removed.
    """
    id_columns = ['ID', 'Id', 'id', 'Unnamed: 0']
    for col in id_columns:
        if col in df.columns:
            return df.drop(columns=[col])
    return df

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

def preprocess_data(filename, bucket_name):
    # Connect to S3
    s3 = boto3.client('s3')

    filename = f"{filename}.csv"

    # Get the weather data file from S3
    obj = s3.get_object(Bucket=bucket_name, Key=filename)

    # Load the weather data into a Pandas DataFrame
    df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
    df = remove_id_column(df)

    df_processed = create_lag_window(df)
    df_processed = df_processed.reset_index(drop=True)

    bucket_name = bucket_name
    key = f"{filename}_processed.csv"

    # Write data to a file on S3
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    s3.put_object(Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=key)
