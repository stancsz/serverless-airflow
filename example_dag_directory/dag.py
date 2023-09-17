from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
import logging

# Default arguments
default_args = {
    'owner': 'me',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime.now() - timedelta(days=1),
}
def print_hello(**kwargs):
    logging.info("Hello from your Cloud Function!")

# Initialize DAG
dag = DAG(
    'my_test_dag2',
    max_active_runs=5,
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Define tasks
start = EmptyOperator(task_id='start', dag=dag)

hello_task = PythonOperator(
    task_id='hello_task',
    python_callable=print_hello,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
start >> hello_task