from typing import List
from sentence_transformers import SentenceTransformer
from google.cloud import bigquery
import pandas_gbq
import time
import os
import sys

PAGE_SIZE = 2000
TOTAL_ROWS = 100000
project_id = os.getenv('PROJECT_ID')
table_name = 'bigquery-public-data.hacker_news.full'
dataset_id = 'genai'
destination_table = f'{dataset_id}.hacker_news_embedded4'

start = time.perf_counter()
model = SentenceTransformer('all-MiniLM-L6-v2')
print(f'---model loaded in : {time.perf_counter() - start} seconds')

def get_embeddings(texts: List[str]) -> List[List[float]]:
    return model.encode(texts).tolist()

def test_embedding():
    start = time.perf_counter()
    embeddings = get_embeddings(['this is an example text']*2000)
    print(type(embeddings))
    print(len(embeddings))
    print(len(embeddings[0]))
    print(f'--- embedding time taken: {time.perf_counter() - start} seconds')

def process_dataframe(df):
    try:
        texts = df['text'].tolist()
        embeddings = get_embeddings(texts)
        df['text_embedding'] = get_embeddings(texts)
        pandas_gbq.to_gbq(dataframe=df, destination_table=destination_table, project_id=project_id, if_exists='append')
    except Exception as e:
        print('an exception occured: ', e)

def read_bigquery_table(table_name: str, year: int = 2022, total_rows: int = TOTAL_ROWS):
    client = bigquery.Client(project=project_id)
    query = f"SELECT id, timestamp, text FROM `{table_name}` WHERE extract(year FROM timestamp) = {year} and text is not null LIMIT {total_rows}"
    job = client.query(query)
    result = job.result(page_size=PAGE_SIZE)

    count = 0

    for df in result.to_dataframe_iterable():
        process_dataframe(df)
        count+=PAGE_SIZE
        print(f'processed: {count} rows')

def main():
    year = 2022
    if len(sys.argv) > 1:
        year = sys.argv[1]
        total_rows = sys.argv[2]

    print(f'processing for year {year} for {total_rows} rows')
    read_bigquery_table(table_name, year, total_rows)

if __name__ == "__main__":
  start = time.perf_counter()
#   test_embedding()
  main()
  print(f'--- TOTAL time taken: {time.perf_counter() - start} seconds')