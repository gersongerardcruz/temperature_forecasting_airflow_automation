import pandas as pd
import boto3
import io 
from openmeteo_py import Hourly, Options, OWmanager
from datetime import datetime

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
