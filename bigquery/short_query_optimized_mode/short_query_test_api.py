#generate python code to invoke a REST API as per below
import requests

url = "https://content-bigquery.googleapis.com/bigquery/v2/projects/nimesa-data/queries"

payload = {
  "jobCreationMode": "JOB_CREATION_OPTIONAL",
  "query": "select current_timestamp()",
  "location": "US"
}

headers = {
  'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, json=payload)

print(response.text)
#print(response.json())