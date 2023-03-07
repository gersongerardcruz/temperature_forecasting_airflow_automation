import pandas as pd
from openmeteo_py import Hourly, Options, OWmanager
from datetime import datetime

def get_weather_data(latitude, longitude, past_days, timezone):
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

    return df

latitude = 14.5995
longitude = 120.9842
past_days = 2
timezone = "Asia/Shanghai"

weather_data = get_weather_data(latitude, longitude, past_days, timezone)
weather_data.to_csv("data/raw/train.csv")