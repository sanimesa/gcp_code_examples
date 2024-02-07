import io
import pandas as pd 
import os
from datetime import datetime
from google.cloud import bigquery
from google.api_core import exceptions
from google.api_core.retry import Retry

project_id = os.environ.get('PROJECT_ID')
dataset_id = os.environ.get('DATASET')

# https://cloud.google.com/bigquery/docs/error-messages

_MY_RETRIABLE_TYPES = (
    exceptions.NotFound, # 404 
    exceptions.TooManyRequests,  # 429
    exceptions.InternalServerError,  # 500
    exceptions.BadGateway,  # 502
    exceptions.ServiceUnavailable,  # 503
)

def is_retryable(exc):
    print(exc)
    return isinstance(exc, _MY_RETRIABLE_TYPES)

def write_to_bq(table_id, rows_to_insert, truncate=False):
    print(f'write_to_bq: {table_id=} {len(rows_to_insert)=} {truncate=}')

    client = bigquery.Client()

    if truncate:
        print(f'truncating target table ...')

        job_config = bigquery.QueryJobConfig(
            priority=bigquery.QueryPriority.INTERACTIVE
        )

        query = "TRUNCATE TABLE `{table_id}`".format(table_id=table_id)
        query_job = client.query(query, job_config=job_config)
        query_job.result() 

    my_retry_policy = Retry(predicate=is_retryable, deadline=300) #required to avoid the table is truncated error
    errors = client.insert_rows_json(table_id, 
                                        rows_to_insert,
                                        retry=my_retry_policy)
    
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))

def table_write_examples():

    ### Example 1: insert a couple of rows, the table needs to exist 
    table_id = f'{project_id}.{dataset_id}.legacy_streaming_example1'

    row1 = {'col1': 1, 'col2': 'foo', 'col3': '2024-02-04'}
    row2 = {'col1': 2, 'col2': 'bar', 'col3': '2024-02-10'}
    rows_to_insert = [row1, row2]
    write_to_bq(table_id, rows_to_insert, truncate=True)

    ### Example 2: Insert nested data, the table needs to exist
    table_id = f'{project_id}.{dataset_id}.legacy_streaming_example2'
    rows_to_insert = [{
                "col1": "1",
                "col2": "second record",
                "col3": '{"a":1,"b":"test"}',
                "col4": {
                    "field1": "1",
                    "field3": "some text value"
                }
    }]
    write_to_bq(table_id, rows_to_insert, truncate=False)

if __name__ == '__main__':
    table_write_examples()



 
    