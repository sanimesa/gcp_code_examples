CREATE OR REPLACE PROCEDURE spark.spark_rest_proc1()
WITH CONNECTION `<PROJECT_ID>.<SPARK_CONNECTION_NAME>`
OPTIONS(engine="SPARK", runtime_version="2.2")
LANGUAGE PYTHON AS R"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import requests
import json
import os 

# Initialize a Spark session
spark = SparkSession.builder \
    .appName("API to BigQuery using UDF") \
    .getOrCreate()

# Sample DataFrame that represents data needing an API call for each row
# You can replace this with actual data you have
data = [("row1", "https://clinicaltrials.gov/api/v2/studies/NCT05364957"),
        ("row2", "https://clinicaltrials.gov/api/v2/studies/NCT03934957"),
        ("row3", "https://clinicaltrials.gov/api/v2/studies/NCT06025357")]

df = spark.createDataFrame(data, ["id", "api_url"])

# Define a function that makes a REST API call
def fetch_data_from_api(api_url):
    try:
        # Log process information (useful to distinguish driver from worker)
        print(f"Executing API call on PID: {os.getpid()} on Host: {os.uname().nodename}")

        response = requests.get(api_url)
        if response.status_code == 200:
            return json.dumps(response.json())  # Return JSON as string
        else:
            return json.dumps({"error": f"Failed with status code {response.status_code}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

# Register the function as a UDF
fetch_data_udf = udf(fetch_data_from_api, StringType())

# Apply the UDF to the DataFrame to create a new column with the API response
df_with_api_data = df.withColumn("api_response", fetch_data_udf(df["api_url"]))

# Print the DataFrame with the API data
df_with_api_data.show(truncate=False)

# Write to BigQuery (replace placeholders with your actual values)
project_id = "nimesa-data"
dataset_id = "spark"
table_id = "clinical_trial_output"

output_table = f"{project_id}.{dataset_id}.{table_id}"

# Write the DataFrame to BigQuery
df_with_api_data.write.format("bigquery") \
  .option("writeMethod", "direct") \
  .mode("overwrite") \
  .save(output_table)


print("Data successfully written to BigQuery")

# Stop the Spark session
# spark.stop()
""";