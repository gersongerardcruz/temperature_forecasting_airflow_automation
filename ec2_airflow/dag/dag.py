import json
from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from utils import get_weather_data, preprocess_data, make_predictions, train_model

# Construct the default_var using the timestamp
default_filename = 'airflow_train'

# Replace bucket_name here with created bucket's name
default_bucket_name = "<bucket_name>"

# Load configuration from the Trigger DAG with Config option
config = Variable.get("config", default_var={}, deserialize_json=True)

# Use config values, or fallback to defaults
filename = config.get("filename", default_filename)
bucket_name = config.get("bucket_name", default_bucket_name)
model_path = config.get("model_path", "model.pkl")
target_column = config.get("target_column", "apparent_temperature")

# Set the Airflow Variables
Variable.set("filename", filename)
Variable.set("bucket_name", bucket_name)
Variable.set("model_path", model_path)
Variable.set("target_column", target_column)


def run_get_data(**op_kwargs):
    # Call the get_weather_data function with the filename and bucket_name arguments
    get_weather_data(filename=filename, bucket_name=bucket_name)

def process_data(**op_kwargs):
    # Call the preprocess data function with the filename and bucket_name arguments
    preprocess_data(filename=filename, bucket_name=bucket_name)

def train(**op_kwargs):
    # Call the train model function with the filename, bucket_name, and target_column arguments
    train_model(filename=filename, bucket_name=bucket_name, target_column=target_column)

def predict(**op_kwargs):
    # Call the make predictions function with the model path and bucket_name arguments
    make_predictions(model_path=model_path, bucket_name=bucket_name, filename=filename, target_column=target_column)

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
    'ml_pipeline',
    default_args=default_args,
    description='Collecting historical weather data, preprocessing, and forecasting',
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

train = PythonOperator(
    task_id='train_model_on_new_data',
    python_callable=train,
    provide_context=True,
    dag=dag
)

predict = PythonOperator(
    task_id='make_predictions_on_processed_data',
    python_callable=predict,
    provide_context=True,
    dag=dag
)

# Create dependency to ensure run_get_data runs first before process_data
run_get_data >> process_data >> train >> predict