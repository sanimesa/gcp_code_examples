#use bigquery python client to load a pandas dataframe into bigquery

from google.cloud import bigquery
import pandas as pd
import os

dataset = os.environ.get('DATASET')

def bigquery_client_library_load_from_dataframe():

    # Create a Pandas DataFrame:
    df = pd.DataFrame(
        {
            "my_string": ["a", "b", "c"],
            "my_int64": [1, 2, 3],
            "my_float64": [4.0, 5.0, 6.0],
            "my_timestamp": [
                pd.Timestamp("1998-09-04T16:03:14"),
                pd.Timestamp("2010-09-13T12:03:45"),
                pd.Timestamp("2015-10-02T16:00:00"),
            ],
            "my_struct": [
                {"field1": 1, "field2": "foo"},
                {"field1": 2, "field2": "bar"},
                {"field1": 3, "field2": "baz"},
            ],
            "my_array" : [{'field1': ['value1', 'value2', 'value3', 'value4']},
                        {'field1': ['value1', 'value2', 'value3', 'value4']},
                        {'field1': ['value1', 'value2', 'value3', 'value4']}
                      ]
        }
    )
    

    # Configure the load job.
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("my_string", "STRING"),
            bigquery.SchemaField("my_timestamp", "TIMESTAMP"),
            bigquery.SchemaField(name="my_struct", field_type="RECORD", fields=[
                    bigquery.SchemaField(name="field1", field_type="INTEGER"),
                    bigquery.SchemaField(name="field2", field_type="STRING")
            ]),
            bigquery.SchemaField("my_array", "RECORD", fields=[
                    bigquery.SchemaField("field1", "STRING", mode="REPEATED")
            ])
        ],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    # Construct a BigQuery client object.
    client = bigquery.Client()
    table_id = f"{dataset}.bigquery_client_library_sample1"

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

    # Wait for the load job to complete.
    job.result()
    print("Loaded {} rows into {}:{}.".format(job.output_rows, client.project, table_id))


if __name__ == '__main__':
    bigquery_client_library_load_from_dataframe()
