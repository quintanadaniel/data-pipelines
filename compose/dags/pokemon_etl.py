import json
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    "owner": "daniel",
    # "email": "prueba@prueba.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def transform_data(**context) -> None:
    task_instance = context["task_instance"]
    data = task_instance.xcom_pull(task_ids="extract_data")
    print(f"data: {data}")
    transformed_data = json.loads(data)['results']
    task_instance.xcom_push(
        key="transformed_data", value=transformed_data
    )


def generate_insert_sql(pokemons: list) -> str:
    insert_sql = """
    INSERT INTO pokemon_data (name, url) VALUES 
    """
    values = [f"('{pokemon['name']}', '{pokemon['url']}')" for pokemon in pokemons]
    insert_sql += ', '.join(values) + ";"
    return insert_sql


def load_data(**kwargs) -> None:
    ti = kwargs['ti']
    pokemons = ti.xcom_pull(task_ids='transform_data_task', key='transformed_data')
    if pokemons:
        insert_sql = generate_insert_sql(pokemons=pokemons)
        ti.xcom_push(key='insert_sql', value=insert_sql)


with DAG(
        "etl_dag_det_pokemons",
        description="ETL to extract pokemons from API and save them to database",
        default_args=default_args,
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024, 7, 6),
        catchup=False,
) as dag:
    is_api_available = HttpSensor(
        task_id="is_api_available",
        http_conn_id="pokeapi",
        endpoint="api/v2/pokemon",
        poke_interval=5,
        timeout=20,
    )

    extract_data = SimpleHttpOperator(
        task_id="extract_data",
        http_conn_id="pokeapi",
        endpoint="api/v2/pokemon",
        method="GET",
        response_filter=lambda response: response.text,
        log_response=True,
    )

    check_table_exist = PostgresOperator(
        task_id="check_table_exist",
        postgres_conn_id="airflow",
        sql="""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'pokemon_data'
            );
        """,
    )

    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="airflow",
        sql="""
        CREATE TABLE IF NOT EXISTS public.pokemon_data (
            name VARCHAR NOT NULL,
            url VARCHAR NOT NULL,
            creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        );
        """,
    )

    transform_data_task = PythonOperator(
        task_id='transform_data_task',
        python_callable=transform_data,
        provide_context=True,
        show_return_value_in_logs=True
    )

    generate_sql_task = PythonOperator(
        task_id='generate_sql_task',
        python_callable=load_data,
        provide_context=True
    )

    load_data = PostgresOperator(
        task_id="load_data",
        postgres_conn_id="airflow",
        sql="{{ ti.xcom_pull(task_ids='generate_sql_task', key='insert_sql') }}",
    )

    end = EmptyOperator(task_id="end", trigger_rule="one_success")

    is_api_available >> extract_data >> check_table_exist >> create_table
    create_table >> transform_data_task >> generate_sql_task >> load_data >> end
