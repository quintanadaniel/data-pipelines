from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# Define a simple function to be used as a task
def my_first_task():
    print("Hello, this is my first Airflow task!")

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# Instantiate the DAG
with DAG(
    'first_dag',
    default_args=default_args,
    description='My first DAG',
    schedule_interval='@daily',
    catchup=False,
) as dag:

    # Define tasks
    start = EmptyOperator(
        task_id='start'
    )

    hello_task = PythonOperator(
        task_id='hello_task',
        python_callable=my_first_task
    )

    end = EmptyOperator(
        task_id='end'
    )

    # Set up task dependencies
    start >> hello_task >> end
