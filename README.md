# Data Pipeline with Python

## Overview

This is a simple project that contain multiples pipeline, with different examples from different files. This is for demostrate the habilities using all the tools as Data Engineer.

## Features

There are some feature we cover in this project:

- Multiple data pipelines for processing distinct datasets.
- Automated data extraction from various sources.
- Transformation and analysis of data using Python, SQL, NoSQL, etc.
- Output results stored in a designated output directory.
- Using Apache Airflow to generate pipelines

## Init the project

- Clone the project

    git clone https://github.com/quintanadaniel/data-pipelines.git

- Acces the project in local

    cd data-pipelines

- Install all requirements

    pip install -r requirements.txt

# Working with Apache Airflow using docker compose.

- For work with Apache Airflow, I created a docker compose image to run postgres, redis, celery executor and apache airflow.
- Then you need to create the following folders to save the information "dags", "logs", "scheduler"

### Step 1: Initialize the Database
Before starting Airflow, you need to initialize the database. Run the following command:

```
docker-compose run --rm webserver airflow db init
```

### Step 2: Start the Services
Start the Airflow services using Docker Compose:

```
docker-compose up -d
```

### Step 3: Access the Airflow Web UI
You can now access the Airflow web interface by navigating to http://localhost:8080 in your web browser. The default username and password are both airflow.

If you have problems, you need to run the following:

1. Check in the Postgres data base, the user and password are correct and exists. If not exists you can create using the following command

    ```
    docker-compose run --rm webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
    ```

2. Check inside the Apache Airflow container the file "airflow.cfg" in the path "/opt/airflow" that you have this line

   ```
   auth_backends = airflow.api.auth.backend.default
   ```

   You can run this command to validate

   ```
   docker copose exec webserver cat airflow.cfg | grep "auth_backends"
   ``` 

3. Make a docker compose up -d to reset the containers.

## Notes

It's very important when we work with airflow, take account the configurations necessaries for example, if you use PostgresOperator and use the attribute 