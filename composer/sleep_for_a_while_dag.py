from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from datetime import timedelta
import time

# Define the DAG
with DAG(
    dag_id='sleep_for_custom_duration',
    description='A manually triggerable DAG that sleeps for a configurable duration',
    schedule_interval=None,  # Manually triggerable
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=int(Variable.get("max_active_runs_sleep_dag", default_var=1)),
    tags=['example', 'sleep', 'configurable'],
) as dag:

    def sleep_task(sleep_time):
        """
        A simple task that sleeps for a specified duration.
        
        :param sleep_time: Duration to sleep in seconds.
        """
        print(f"Task started: Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)
        print(f"Task completed: Woke up after {sleep_time} seconds.")

    sleep_interval = int(Variable.get("sleep_interval_seconds", default_var=300))  # Default to 300 seconds (5 minutes) if not set

    sleep_operator = PythonOperator(
        task_id='sleep_task',
        python_callable=sleep_task,
        op_kwargs={'sleep_time': sleep_interval},
    )

    sleep_operator
