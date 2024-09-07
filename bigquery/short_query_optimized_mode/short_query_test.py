import timeit
from google.cloud import bigquery


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


time = timeit.timeit(run_query, number=100)
print("Time taken: {}".format(time))