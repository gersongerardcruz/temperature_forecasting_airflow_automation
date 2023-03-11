from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from get_data import *

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'collect_data_dag',
    default_args=default_args,
    description='Collecting historical weather data'
)

run_get_data = PythonOperator(
    task_id="collect_weather_data",
    python_callable=run_get_weather_data,
    dag=dag
)

run_get_data
