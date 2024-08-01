from vertexai.language_models import TextEmbeddingModel
from google.cloud import bigquery
import time
import os

project_id = os.environ.get('PROJECT_ID')  
table_name = 'bigquery-public-data.hacker_news.full'
year = 2022

def read_bigquery_table(table_name: str) -> list:
    client = bigquery.Client()
    query = f"SELECT id, timestamp, text FROM `{table_name}` where extract(year FROM timestamp) = {year}  limit 500"
    job = client.query(query)
    result = job.result(page_size=100) 

    for df in result.to_dataframe_iterable():
        # df will have at most 20 rows
        print(f"Number of rows: {len(df)}")
        print(df)
        process_data(df)

def process_data(df):
    content = df['text'].tolist()
    embeddings = text_embedding(content)
    #create a new datafrom from the df and add the embeddings as a new column 
    df['text_embedding'] = embeddings
    print(df)
    print(df.dtypes)
    # write the df to a new table
    df.to_gbq(f'genai.hacker_news_embedded', project_id=project_id, if_exists='append')

def text_embedding(content: list) -> list:
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = [embedding.values for embedding in model.get_embeddings(content)]

    return embeddings
    # for embedding in embeddings:
    #     vector = embedding.values
    #     print(f"Length of Embedding Vector: {len(vector)}")
    # return vector

if __name__ == "__main__":
    start_time = time.time()
    # text_embedding()
    read_bigquery_table(table_name)
    print("--- %s seconds ---" % (time.time() - start_time))