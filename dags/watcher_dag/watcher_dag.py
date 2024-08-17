from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def helloWorld():
    print("Hello")


with DAG(dag_id="helloworlddag",
         start_date=datetime(2021, 1, 1),
         schedule_interval="@hourly",
         catchup=False) as dag:
    task1 = PythonOperator(
        task_id="helloworld",
        python_callable=helloWorld)
task1
