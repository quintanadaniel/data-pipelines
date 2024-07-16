from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
  'owner': 'daniel quintana',
  'start_date': datetime(2024, 7, 5),
  'retries': 1
}

with DAG('codependency', default_args=default_args) as codependency_dag:

    bash_example = BashOperator(
        task_id="bash_example",
        bash_command='echo "Example second dags using BashOperator"',
        dag=codependency_dag
    )

    get_one_pokemon = BashOperator(
        task_id='get_one_pokemon',
        bash_command='get_one_pokemon.sh',
        dag=codependency_dag
    )

    # Define a final operator to execute the `push_data.sh` script
    pull_pokemons = BashOperator(
        task_id="pull_pokemons_task",
        bash_command="wget https://pokeapi.co/api/v2/pokemon/",
        dag=codependency_dag)


    # Set up task dependencies
    bash_example >> get_one_pokemon << pull_pokemons
