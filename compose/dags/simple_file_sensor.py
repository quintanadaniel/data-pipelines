import logging
import os

from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.utils.dates import days_ago

default_args = {
    "owner": "daniel quintana"
}

with DAG(
        dag_id="simple_file_sensor",
        description="Running a simple file sensor",
        default_args=default_args,
        schedule_interval="@once",
        start_date=days_ago(1),
        tags=["python", "sensor", "file sensor"]
) as dag:

    logging.info(f"Checking for file at {os.listdir(os.path.join(os.getcwd(),'tmp'))}")

    checking_for_file = FileSensor(
        task_id="checking_for_file",
        filepath="tmp/review_data.csv",
        poke_interval=15,
        timeout=60 * 10,
        mode="poke"
    )

    checking_for_file
