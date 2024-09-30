from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from datetime import timedelta
import pandas as pd
import numpy as np
import time
import logging
import string
import random

# Define the DAG
with DAG(
    dag_id='heavy_cpu_consumption_dag',
    description='A manually triggerable DAG that performs heavy data processing using Pandas',
    schedule_interval=None,  # Manually triggerable
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=int(Variable.get("max_active_runs_heavy_dag", default_var=1)),
    tags=['example', 'heavy', 'cpu', 'pandas'],
) as dag:

    def generate_random_strings(n, length=10):
        """Generate an array of random strings of fixed length."""
        return [''.join(random.choices(string.ascii_letters, k=length)) for _ in range(n)]


    # Define the Python callable
    def heavy_data_processing(data_size: int, num_iterations: int):

        logging.info(f"Starting heavy data processing with data_size={data_size} and num_iterations={num_iterations}")

        # Step 1: Generate a large DataFrame
        logging.info("Generating large DataFrame...")
        start_time = time.time()
        df = pd.DataFrame({
            'A': np.random.randint(0, 100, size=data_size),
            'B': np.random.randint(0, 100, size=data_size),
            'C': np.random.randn(data_size),
            'D': generate_random_strings(data_size)
        })
        logging.info(f"DataFrame generated in {time.time() - start_time:.2f} seconds.")

        # Step 2: Perform heavy computations
        logging.info("Starting heavy computations...")
        start_time = time.time()
        for i in range(num_iterations):
            # Replace negative values in 'C' with a small positive value
            df['C'] = df['C'].apply(lambda x: x if x > -1 else -1 + 1e-9)

            # Example computation: complex calculations and DataFrame manipulations
            df['E'] = df['A'] * df['B'] + np.log1p(df['C'])
            df['F'] = df['E'].rolling(window=100).mean()
            df['G'] = df['F'].apply(lambda x: x ** 2 if pd.notnull(x) else x)
            if i % 10 == 0:
                logging.info(f"Completed {i} iterations.")
        
        logging.info(f"Heavy computations completed in {time.time() - start_time:.2f} seconds.")

        # Step 3: Aggregate results
        logging.info("Aggregating results...")
        start_time = time.time()
        summary = df.describe()
        logging.info(f"Aggregation completed in {time.time() - start_time:.2f} seconds.")
        logging.info(f"Data Summary:\n{summary}")

        logging.info("Heavy data processing task completed successfully.")

    # Retrieve parameters from Airflow Variables
    data_size = int(Variable.get("data_size", default_var=1_000_000))  # Default to 1,000,000 rows
    num_iterations = int(Variable.get("num_iterations", default_var=100))  # Default to 100 iterations

    # Define the PythonOperator
    heavy_processing_task = PythonOperator(
        task_id='heavy_data_processing',
        python_callable=heavy_data_processing,
        op_kwargs={
            'data_size': data_size,
            'num_iterations': num_iterations,
        },
        dag=dag,
    )

    # Since there's only one task, no need to set dependencies
    heavy_processing_task