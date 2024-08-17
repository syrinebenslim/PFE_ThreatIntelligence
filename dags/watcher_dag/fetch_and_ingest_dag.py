from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from watcher.callerapi.misp.main_transformation_misp import main
from watcher.callerapi.misp.reader import MispReader

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0

}


def execute_main():
    reader = MispReader("https://www.botvrij.eu/data/feed-osint")
    df = reader.write_misp_events()
    if df is not None:
        print(df.info())
    else:
        print("DataFrame is None")


def execute_main1():
    main()


with DAG(
        'fetch_and_ingest',
        default_args=default_args,
        description='Fetch and ingest data from API',
        schedule_interval="@daily",
        max_active_runs=1,
        catchup=False
) as dag:
    run_fetch_and_ingest = PythonOperator(
        task_id='fetch_and_ingest',
        python_callable=execute_main
    )
    transform_orga_event = PythonOperator(
        task_id='transform_org_event',
        python_callable=execute_main1
    )

    run_fetch_and_ingest >> transform_orga_event
