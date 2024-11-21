# Please include only Python code here. When you click RUN or SAVE, a stored procedure is created using this Python code.
# This code copies a Postgres table to BigQuery. Please adjust parameters and dataset / table names as needed 
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, to_timestamp, regexp_replace
from pyspark.sql.types import TimestampType
import os
import json 

# Create a Spark session
spark = SparkSession.builder.appName("PostgresToBigQuery").getOrCreate()

# Parse the params (set this in the PySpark Options)
postgres_url = json.loads(os.environ['BIGQUERY_PROC_PARAM.postgres_url'])
postgres_user = json.loads(os.environ['BIGQUERY_PROC_PARAM.postgres_user'])
postgres_password = json.loads(os.environ['BIGQUERY_PROC_PARAM.postgres_password'])

# Read data from Postgres
postgres_df = spark.read \
    .format("jdbc") \
    .option("url", postgres_url) \
    .option("driver", "org.postgresql.Driver") \
    .option("user", postgres_user) \
    .option("password", postgres_password) \
    .option("dbtable", "employees") \
    .load()

# Create a new column with a constant value
postgres_df = postgres_df.withColumn("manager", lit("Eric Johnson"))

# Define BigQuery connection parameters
project_id = "nimesa-data"
dataset_id = "spark"
table_id = "postgres_employees_output"

output_table = f"{project_id}.{dataset_id}.{table_id}"

# Write the DataFrame to BigQuery
postgres_df.write.format("bigquery") \
  .option("writeMethod", "direct") \
  .mode("overwrite") \
  .save(output_table)


print("Data successfully written to BigQuery")