import random
import time
from google.cloud import bigquery
from datetime import datetime
import os

project_id = os.environ.get('PROJECT_ID')
dataset = os.environ.get('DATASET')

# Initialize BigQuery client
client = bigquery.Client()

# Configurable parameters
num_instruments = 10
metrics = ["temperature", "pressure", "humidity"]  # Add any other metrics as needed
table_id = f"{project_id}.{dataset}.instrument_data"  # Replace with your BigQuery table

# Function to generate mock data for a single instrument
def generate_instrument_data(instrument_id):
    data = {
        "instrument_id": instrument_id,
        # "timestamp": datetime.utcnow().isoformat(),
    }
    for metric in metrics:
        data[metric] = round(random.uniform(20.0, 100.0), 2)  # Random value between 20 and 100
    return data

# Function to insert data into BigQuery
def insert_into_bigquery(rows_to_insert):
    errors = client.insert_rows_json(table_id, rows_to_insert)  # Insert JSON data
    if errors:
        print(f"Errors: {errors}")
    else:
        print(f"Inserted {len(rows_to_insert)} rows.")

# Main function to generate and insert data
def main():
    while True:
        rows = []
        for i in range(1, num_instruments + 1):
            instrument_data = generate_instrument_data(f"instrument_{i}")
            rows.append(instrument_data)
        
        insert_into_bigquery(rows)
        
        # Random sleep time between 1 to 5 seconds
        sleep_time = random.randint(3, 30)
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
