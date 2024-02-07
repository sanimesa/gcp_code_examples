--- bigquery python client examples
CREATE TABLE <schema_name>.bigquery_client_library_sample1
(
  my_string STRING,
  my_int64 INT64,
  my_float64 FLOAT64,
  my_timestamp TIMESTAMP,
  my_struct STRUCT<field1 INT64, field2 STRING>,
  my_array STRUCT<field1 ARRAY<STRING>>
);

-- for the legacy streaming examples
create table <schema_name>.legacy_streaming_example1 (
    col1 INTEGER,
    col2 STRING,
    col3 DATE
);

CREATE TABLE <schema_name>.legacy_streaming_example2 (
  col1 INT64,
  col2 STRING,
  col3 JSON,
  col4 STRUCT<field1 INT64, field3 STRING>
);

-- ODBC example
CREATE TABLE <schema_name>.bq_odbc_test
(
  id INT64,
  name STRING
);

-- JDBC example
CREATE TABLE   <schema_name>.test_jdbc
(
  column1 STRING,
  column2 INT64
);