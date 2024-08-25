import os

import pandas as pd
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago


default_args = {
    "owner": "daniel quintana"
}

def read_csv_file():
    df = pd.read_csv("./input_files/apps_data.csv")

    print(df)

    return df.to_json()

def determine_branch():
    final_output = Variable.get("transform", default_var=None)

    if final_output == 'filter_art_and_design':
        return 'filter_art_and_design_task'
    elif final_output == 'filter_events':
        return 'filter_events_task'

def filter_art_and_design(ti):
    json_data = ti.xcom_pull(task_ids="read_csv_filename_task")

    df = pd.read_json(json_data)

    art_and_design = df[df["Category"] == 'ART_AND_DESIGN']

    ti.xcom_push(key='transform_result', value=art_and_design.to_json())
    ti.xcom_push(key='transform_filename', value='art_and_design')

def filter_events(ti):
    json_data = ti.xcom_pull(task_ids="read_csv_filename_task")

    df = pd.read_json(json_data)

    events = df[df["Category"] == 'EVENTS']

    ti.xcom_push(key='transform_result', value=events.to_json())
    ti.xcom_push(key='transform_filename', value='events')


def write_csv_file(ti):
    json_data = ti.xcom_pull(key='transform_result')
    file_name = ti.xcom_pull(key='transform_filename')

    df = pd.read_json(json_data)
    df.to_csv(f"./output_files/{file_name}.csv", index=False)


with DAG(
    dag_id="branching_using_operators",
    description="Branching using operators",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@once",
    tags=["branching", "python", "operators"]
) as dag:
    read_csv_file_task = PythonOperator(
        task_id="read_csv_filename_task",
        python_callable=read_csv_file
    )

    determine_branch_task = BranchPythonOperator(
        task_id="determine_branch_task",
        python_callable=determine_branch
    )

    filter_art_and_design_task = PythonOperator(
        task_id="filter_art_and_design_task",
        python_callable=filter_art_and_design
    )

    filter_events_task = PythonOperator(
        task_id="filter_events_task",
        python_callable=filter_events
    )

    write_csv_file_task = PythonOperator(
        task_id="write_csv_filename_task",
        python_callable=write_csv_file,
        trigger_rule="none_failed"
    )

read_csv_file_task >> determine_branch_task >> [filter_art_and_design_task, filter_events_task] >> write_csv_file_task