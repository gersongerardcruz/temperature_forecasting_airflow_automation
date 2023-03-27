import json
from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from utils import get_weather_data, preprocess_data

# Construct the default_var using the timestamp
default_filename = f'airflow_train'
default_bucket_name = "airflow-gerson"

# Load configuration from the Trigger DAG with Config option
config = Variable.get("config", default_var={}, deserialize_json=True)

# Use config values, or fallback to defaults
filename = config.get("filename", default_filename)
bucket_name = config.get("bucket_name", default_bucket_name)

# Set the Airflow Variables
Variable.set("filename", filename)
Variable.set("bucket_name", bucket_name)

def run_get_data(**op_kwargs):
    # Call the get_weather_data function with the filename and bucket_name argument
    get_weather_data(filename=filename, bucket_name=bucket_name)

def process_data(**op_kwargs):
    # Call the preprocess data function with the filename and bucket_name argument
    preprocess_data(filename=filename, bucket_name=bucket_name)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

dag = DAG(
    'collect_data_dag',
    default_args=default_args,
    description='Collecting historical weather data',
    schedule_interval=None
)

run_get_data = PythonOperator(
    task_id="collect_weather_data",
    python_callable=run_get_data,
    provide_context=True,
    op_kwargs={
        'filename': filename, 
        'bucket_name': bucket_name
    },
    dag=dag
)

process_data = PythonOperator(
    task_id='preprocess_data',
    python_callable=process_data,
    provide_context=True,
    dag=dag
)

# Create dependency to ensure run_get_data runs first before process_data
run_get_data >> process_data
