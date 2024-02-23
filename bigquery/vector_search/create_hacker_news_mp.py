from concurrent.futures import ThreadPoolExecutor
from vertexai.language_models import TextEmbeddingModel
from google.cloud import bigquery
import time
import os
from text_embeddings import TextEmbeddingClient

project_id = os.environ.get('PROJECT_ID')  
dataset_id = os.environ.get('DATASET_ID')
table_name = 'bigquery-public-data.hacker_news.full'
destination_table = f'{dataset_id}.hacker_news_embedded2'
print(destination_table)

MAX_WORKERS = 20
TOTAL_ROWS = 2000
PAGE_SIZE = 2000
BATCH_SIZE = 100

text_embedding_client = TextEmbeddingClient(TextEmbeddingClient.EMBEDDING_MODEL_OPENAI_SMALL)

def text_embedding(content: list) -> list:
    embeddings = None

    try: 
        start = time.perf_counter()
        embeddings = text_embedding_client.get_embedding(content)
        print(f"text embedding: {time.perf_counter() - start} seconds ---")
    except Exception as e:
        print(e)
    
    if embeddings is None:
        print("embedding failed, just pass 0s for now but Cosine search will fail, use Euclide search instead or clean up data")
        return [ [0]*text_embedding_client.get_embedding_dim() for i in range(len(content))]
    else:
        return embeddings

def list_iterator(lst, chunk_size=100):
    chunk_size = max(1, chunk_size)
    
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i+chunk_size]

def process_dataframe(df):
    content = df['text'].tolist()
    embeddings = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        chunked_content = list(list_iterator(content, chunk_size=BATCH_SIZE))
        futures = [executor.submit(text_embedding, chunk) for chunk in chunked_content]

        for future in futures:
            embedding_result = future.result()
            embeddings.extend(embedding_result)

    df['text_embedding'] = embeddings

    start = time.perf_counter()
    df.to_gbq(destination_table, project_id=project_id, if_exists='append')
    print(f"persistence:{time.perf_counter() - start} seconds ---")

def read_bigquery_table(table_name: str, year: int = 2022):
    client = bigquery.Client()
    query = f"SELECT id, timestamp, text FROM `{table_name}` WHERE extract(year FROM timestamp) = {year} LIMIT {TOTAL_ROWS}"
    job = client.query(query)
    result = job.result(page_size=PAGE_SIZE)

    for df in result.to_dataframe_iterable():
        process_dataframe(df)   

if __name__ == "__main__":
    start_time = time.time()
    read_bigquery_table(table_name, 2019)
    print("--- %s seconds ---" % (time.time() - start_time))


