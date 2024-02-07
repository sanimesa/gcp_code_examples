**Overview**

Example code to demonstrate how to use the pandas-gbq and google-cloud-bigquery libraries to read and write data to BigQuery.

Install the required libraries from the requirements.txt.
Obtain a service account key file from the Google Cloud Console.
The service account should have editor access on the dataset you plan to use.
Please use keys and permissions securely and do not share them.


The below environment variables need to be set for the samples to run:

    GOOGLE_APPLICATION_CREDENTIALS=<path to service account key>
    GOOGLE_CLOUD_PROJECT=<project id>
    GOOGLE_CLOUD_REGION=<region>
    PROJECT_ID=<project id>
    DATASET=<dataset>

Please note that you will need a google clour project properly configured, a service account key and a dataset.
There might be cloud computing charges if you use this samples. 

To run the ODBC/JDBC samples, you will need to install the appropriate drivers and configure them.
https://cloud.google.com/bigquery/docs/reference/odbc-jdbc-drivers

The JDBC sample can be run with the following command sets from google cloud shell:

    curl -o SimbaJDBCDriverforGoogleBigQuery42_1.5.2.1005.zip https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.5.2.1005.zip
    unzip SimbaJDBCDriverforGoogleBigQuery42_1.5.2.1005.zip -d ./bqjava
    javac WriteToBigQuery.java
    java -classpath bqjava/*:. WriteToBigQuery
