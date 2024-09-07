import timeit
from google.cloud import bigquery
import sys
import os

query = """
    SELECT current_timestamp()
"""

client = bigquery.Client()

def run_query():

    rows = client.query_and_wait(query)

    if rows.job_id is not None:
        print("Query was run with job state.  Job ID: {}".format(rows.job_id))
    else:
        print("Query was run in short mode.  Query ID: {}".format(rows.query_id))


#run with the optimization
os.environ['QUERY_PREVIEW_ENABLED'] = 'TRUE'
time_opt  = timeit.timeit(run_query, number=100)

#run without the optimization
os.environ['QUERY_PREVIEW_ENABLED'] = 'FALSE'
time_no = timeit.timeit(run_query, number=100)

print(f"Time taken with optimization: {time_opt:.2f}" )
print(f"Time taken without optimization: {time_no:.2f}")