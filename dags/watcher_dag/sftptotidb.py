from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator

from watcher.entry_point_sftp_listener import main as main_sftp
from watcher.shadow_transformation_refined import ShadowTransformationRefined

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0

}


def execute_main_transformation():
    vul_types = Variable.get("vul_types")
    if vul_types:
        ShadowTransformationRefined(vul_types).refine()


def execute_main_sftp():
    main_sftp()


with DAG(
        'shadow_pipeline',
        default_args=default_args,
        description='Fetch and ingest data from SFDTP to TIDB',
        schedule_interval="@daily",
        max_active_runs=1,
        catchup=False
) as dag:
    run_fetch_and_ingest = PythonOperator(
        task_id='sftp_integration',
        python_callable=execute_main_sftp
    )
    transform_shadow_data = PythonOperator(
        task_id='transform data',
        python_callable=execute_main_transformation
    )

    run_fetch_and_ingest >> transform_shadow_data
