# Apache Airflow

## 1) Why Airflow?

Apache Airflow is useful when you need to orchestrate multiple data or engineering tasks with clear dependencies, retries, and schedules.

- Workflow as code: Define DAGs in Python, version control them, and review changes.
- Dependency management: Explicit task ordering (`A >> B >> C`) and branching.
- Scheduling + backfill: Run hourly/daily jobs and re-run historical windows.
- Observability: UI shows task status, logs, retries, and execution timeline.
- Extensible ecosystem: Operators/hooks for AWS, GCP, Snowflake, dbt, Spark, Kubernetes, and more.
- Reliability features: Retries, SLAs, alerts, and failure handling.

When Airflow is a strong fit:
- ETL/ELT pipelines
- Analytics/reporting pipelines
- ML/data preparation pipelines
- Cross-system batch orchestration

When not ideal:
- Very simple single-step jobs
- Ultra-low-latency event processing (event-driven services can be better)

## 2) Internal Working

At a high level, Airflow has four core runtime components:

- Webserver: UI for DAG visibility, logs, and manual triggers.
- Scheduler: Parses DAG files and decides which tasks are ready to run.
- Metadata DB: Stores DAG runs, task instances, states, variables, connections.
- Executor + Workers: Actually run tasks (LocalExecutor/CeleryExecutor/KubernetesExecutor).

Execution flow (simplified):

1. You place a DAG Python file in the DAGs folder.
2. Scheduler parses DAGs and creates DAG Runs based on schedule/trigger.
3. Scheduler checks dependencies and marks runnable tasks.
4. Executor queues/runs tasks on workers.
5. Task state and logs are written to metadata DB and log backend.
6. UI reflects real-time states (queued/running/success/failed).
7. Retries/alerts trigger according to DAG/task settings.

Key concepts:

- DAG: Directed Acyclic Graph that defines workflow.
- Task: Single unit of work inside a DAG.
- DAG Run: One execution of the full DAG for a logical date.
- Task Instance: One run of one task in one DAG Run.
- XCom: Small messages between tasks.

## 3) Setting Up and Starting Demo

### Option A: Fastest (Docker)

Prerequisites:
- Docker Desktop installed and running
- At least 4 GB RAM available for Docker

Steps:

1. Create a working folder and move into it.
2. Download the official `docker-compose.yaml` for Airflow.
3. Initialize Airflow metadata DB.
4. Start Airflow services.
5. Open UI at `http://localhost:8080`.

Commands:

```bash
mkdir airflow-demo && cd airflow-demo
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins ./config

echo "AIRFLOW_UID=50000" > .env

Remove-Item .env -ErrorAction SilentlyContinue
Set-Content -Path .env -Value 'AIRFLOW_UID=50000' -NoNewline -Encoding ascii
docker compose up airflow-init


docker compose up airflow-init
docker compose up -d
```

Default login (in official quick-start):
- Username: `airflow`
- Password: `airflow`

### Create a Demo DAG

Create file: `./dags/demo_pipeline.py`

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def extract():
    print("Extract step")


def transform():
    print("Transform step")


def load():
    print("Load step")


with DAG(
    dag_id="demo_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["demo"],
) as dag:
    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load", python_callable=load)

    t1 >> t2 >> t3
```

Start demo run:
1. Open Airflow UI.
2. Enable `demo_pipeline` DAG.
3. Click Trigger DAG.
4. Open Graph view and task logs.

### Stop Demo

```bash
docker compose down
```

---

Summary:
- Airflow is best for scheduled, dependency-heavy data workflows.
- Internally, scheduler + executor + workers run tasks while metadata DB tracks state.
- You can start quickly with Docker and run a first DAG in minutes.
