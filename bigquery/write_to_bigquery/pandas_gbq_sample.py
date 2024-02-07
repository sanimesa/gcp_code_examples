import pandas as pd
import pandas_gbq
import os
from datetime import datetime

dataset = os.environ.get('DATASET')

def write_to_bigquery_examples():

    ### Example 1: create a simple table from a dataframe, let pandas-gbq infer data types 
    df = pd.DataFrame({'col1': [1, 2], 
                       'col2': ['test', 'test'], 
                       'col3': [datetime.now(), datetime.now()]})
    
    pandas_gbq.to_gbq(df, 
                      f'{dataset}.pandas_gbq_example1', 
                      if_exists='append')

    ### Example 2: create a simple table from a dataframe, let pandas-gbq infer data types 
    df = pd.DataFrame({'col1': [1, 2], 
                       'col2': ['test', 'test'], 
                       'col3': ['2024-01-10', '2024-01-11']})
    
    pandas_gbq.to_gbq(df, 
                      f'{dataset}.pandas_gbq_example2', 
                      if_exists='append')

    ### Example 3: create a simple table from a dataframe, provide a schema so the DATE columns gets the proper data type
    pandas_gbq_example3_schema =  [{"name":"col1","type":"INTEGER"},
                                   {"name":"col2","type":"STRING"},
                                   {"name":"col3","type":"DATE"}]

    df = pd.DataFrame({'col1': [1, 2], 
                       'col2': ['test', 'test'], 
                       'col3': ['2024-01-10', '2024-01-11']})
    
    pandas_gbq.to_gbq(df, 
                      f'{dataset}.pandas_gbq_example3', 
                      table_schema=pandas_gbq_example3_schema,
                      if_exists='fail')

    #-- this also works since the string can get cast into a BigQuery data 
    pandas_gbq.to_gbq(df, 
                      f'{dataset}.pandas_gbq_example3', 
                      if_exists='append')


    ### Example 4: create a simple table from a dataframe, provide a schema so the TIMESTAMP columns gets the proper data type
    pandas_gbq_example4_schema =  [{"name":"col1","type":"INTEGER"},
                                   {"name":"col2","type":"STRING"},
                                   {"name":"col3","type":"TIMESTAMP"}]

    df = pd.DataFrame({'col1': [1, 2], 
                       'col2': ['test', 'test'], 
                       'col3': ['2024-01-10 10:00:00', '2024-01-11 10:00:00']})
    
    df['col3'] = pd.to_datetime(df['col3']) #need to convert to timestamp for it to work 
    
    pandas_gbq.to_gbq(df, 
                      f'{dataset}.pandas_gbq_example4', 
                      table_schema=pandas_gbq_example4_schema,
                      if_exists='fail')

    pandas_gbq.to_gbq(df, 
                      f'{dataset}.pandas_gbq_example4', 
                      table_schema=pandas_gbq_example4_schema,
                      if_exists='append')


    ### Example 5: column names must confirm to BigQuery column naming conventions 
    df = pd.DataFrame({'Customer Id': [1, 2], 
                       'Customer Name': ['Easy Movers', 'Supplies Inc'], 
                       'Annual Revenue (2020)': ['50000', '75000']})
    
    #--- need this to make the column names compliant with BigQuery 
    df.columns = [col.replace(' ', '_').replace('(', '_').replace(')', '_') for col in df.columns]

    pandas_gbq.to_gbq(df, 
                      f'{dataset}.pandas_gbq_example5', 
                      if_exists='append')


    # Example 6: Write DataFrame with a nested structure: in older versions of pandas-gbq, need to create the table first 
    data = {
        'id': [1, 2],
        'record_col': [{'field1': 'value1', 'field2': 10}, {'field1': 'value2', 'field2': 20}],
        'array_col': [{'field1': ['value1', 'value2', 'value3', 'value4']},
                      {'field1': ['value1', 'value2', 'value3', 'value4']}]
    }

    df = pd.DataFrame(data)

    # Define the BigQuery schema, including the RECORD type
    nested_schema = [
        {'name': 'id', 'type': 'INTEGER'},
        {'name': 'record_col', 'type': 'RECORD', 'fields': [
            {'name': 'field1', 'type': 'STRING'},
            {'name': 'field2', 'type': 'INTEGER'}
        ]},
        {
            "name": "array_col",
            "type": "RECORD",
            "fields": [
                {
                    "name": "field1",
                    "mode": "REPEATED",
                    "type": "STRING",
                }
            ]
        }
    ]

    pandas_gbq.to_gbq(df, f'{dataset}.pandas_gbq_example6', 
                      table_schema=nested_schema, if_exists='replace')

def main():
    write_to_bigquery_examples()

if __name__ == '__main__':
    main()