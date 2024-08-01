import multiprocessing
from vertexai.language_models import TextEmbeddingModel
from google.cloud import bigquery
import time
import os

project_id = os.environ.get('PROJECT_ID')  
dataset_id = os.environ.get('DATASET_ID')
table_name = 'bigquery-public-data.hacker_news.full'

MULTIPROCESSING_POOL_SIZE = 10
TOTAL_ROWS = 2000
PAGE_SIZE = 1000
BATCH_SIZE = 100

model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001") #the higher models get throttled 

def text_embedding(content: list) -> list:
    start = time.perf_counter()
    embeddings = [embedding.values for embedding in model.get_embeddings(content)]
    print(f"text embedding: {time.perf_counter() - start} seconds ---")
    return embeddings

def process_dataframe(df):
    content = df['text'].tolist()
    embeddings = text_embedding(content)
    df['text_embedding'] = embeddings
    start = time.perf_counter()
    df.to_gbq(f'genai.hacker_news_embedded', project_id=project_id, if_exists='append')
    print(f"persistence:{time.perf_counter() - start} seconds ---")

def dataframe_iterator(df, chunk_size=100):
    chunk_size = max(1, chunk_size)
    
    # Total number of rows in the DataFrame
    total_rows = len(df)
    
    for start in range(0, total_rows, chunk_size):
        end = start + chunk_size
        yield df.iloc[start:end]

def read_bigquery_table(table_name: str, year: int = 2022):
    client = bigquery.Client()
    query = f"SELECT id, timestamp, text FROM `{table_name}` WHERE extract(year FROM timestamp) = {year} LIMIT {TOTAL_ROWS}"
    job = client.query(query)
    result = job.result(page_size=PAGE_SIZE)

    with multiprocessing.Pool(MULTIPROCESSING_POOL_SIZE) as pool:
        for df in result.to_dataframe_iterable():
            start = time.perf_counter()
            it = list(dataframe_iterator(df, chunk_size=100))
            print(f"data read: {time.perf_counter() - start} seconds ---")
            pool.map(process_dataframe, it)

if __name__ == "__main__":
    start_time = time.time()
    # text_embedding()
    read_bigquery_table(table_name)
    print("--- %s seconds ---" % (time.time() - start_time))


