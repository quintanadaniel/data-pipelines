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

# Working with Apache Airflow using docker compsoe.

- For work with Apache Airflow, I created a docker compose image to run postgres, redis, celery executor and apache airflow.

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

