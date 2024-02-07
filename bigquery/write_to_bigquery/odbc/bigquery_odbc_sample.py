import pyodbc
import time 
import os 

dataset = os.environ.get('DATASET')

# create table <dataset>.bq_odbc_test (
#   id INTEGER,
#   name STRING
# );

def get_connection():
    cnxn = pyodbc.connect("DSN=bigquery")
    cnxn.autocommit = True

    return cnxn

def insert_data():

    with get_connection() as cnxn:
        cursor = cnxn.cursor()
        sql = f"INSERT INTO {dataset}.bq_odbc_test (id, name) VALUES (?, ?)"
        params = [(i,'some name') for i in range(10)]
        t0 = time.perf_counter()
        cursor.executemany(sql, params)
        print(f'inserted 10 rows in {time.perf_counter() - t0:.1f} seconds')

if __name__ == '__main__':
    insert_data()