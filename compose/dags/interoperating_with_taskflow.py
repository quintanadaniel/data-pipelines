import time

import pandas as pd
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.operators.python import BranchPythonOperator, PythonOperator

default_args = {
    "owner": "daniel quintana"
}


@dag(
    dag_id="interoperating_with_taskflow",
    description="Interoperating using TaskFlow API",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@once",
    tags=["interop", "python", "taskflow", "operators"]
)
def interoperating_with_taskflow_api():

    def read_csv_file(ti):
        df = pd.read_csv("./input_files/apps_data.csv")

        print(df)

        #return df.to_json()
        ti.xcom_push(key="original_data", value=df.to_json())

    @task
    def filtering_photography(json_data):

        df = pd.read_json(json_data)

        photography = df[df["Category"] == "PHOTOGRAPHY"]

        return photography.to_json()

    def write_csv_file(filtered_photography_json):

        df = pd.read_json(filtered_photography_json)
        df.to_csv("./output_files/photography.csv", index=False)

    read_csv_file_task = PythonOperator(
        task_id="read_csv_filename_task",
        python_callable=read_csv_file
    )

    #filtered_photography_json = filtering_photography(read_csv_file_task.output)
    filtered_photography_json = filtering_photography(read_csv_file_task.output["original_data"])

    write_csv_file_task = PythonOperator(
        task_id="write_csv_filename_task",
        python_callable=write_csv_file,
        trigger_rule="none_failed",
        op_kwargs={"filtered_photography_json": filtered_photography_json}
    )


interoperating_with_taskflow_api()
