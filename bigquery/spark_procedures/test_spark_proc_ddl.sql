-- adjust the dataset name, here it is simply called spark
CREATE OR REPLACE PROCEDURE spark.spark_basic_test_proc(test_parm INT64, OUT avg_salary FLOAT64)
WITH CONNECTION `<PROJECT_ID>.<SPARK_CONNECTION_NAME>`
OPTIONS(engine="SPARK", runtime_version="2.2")
LANGUAGE PYTHON AS R"""

from pyspark.sql import SparkSession
from bigquery.spark.procedure import SparkProcParamContext
from pyspark.sql.functions import col, avg, sum, count, lit
import os
import json

# IN Parameters are available from environment variables 
test_parm = os.environ['BIGQUERY_PROC_PARAM.test_parm']
print(f"The parameter: {test_parm} is of type: {type(test_parm)}")

# Initialize a Spark session
spark = SparkSession.builder \
    .appName("Basic Spark Script") \
    .getOrCreate()

spark_proc_param_context = SparkProcParamContext.getOrCreate(spark)

# Create a DataFrame with fake data
data = [
    ("Alice", 34, "Engineer", 75000),
    ("Bob", 28, "Analyst", 60000),
    ("Catherine", 45, "Manager", 95000),
    ("David", 35, "Engineer", 80000),
    ("Eva", 29, "Analyst", 65000)
]
columns = ["Name", "Age", "Position", "Salary"]

df = spark.createDataFrame(data, schema=columns)

# Show the DataFrame
print("Original DataFrame:")
df.show()

# Calculate the average salary
avg_salary_df = df.select(avg(col("Salary")).alias("Average Salary"))
print("Average Salary:")
avg_salary_df.show()

# Out parameters are set like ths 
spark_proc_param_context.avg_salary = avg_salary_df.collect()[0]["Average Salary"]

# Stop the Spark session - commented since the out parameter assignment does not work
# spark.stop()
""" 
;