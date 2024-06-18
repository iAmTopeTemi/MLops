import os
import requests

# Get Databricks host and token from environment variables
os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')
databricks_host = os.getenv('DATABRICKS_HOST')
databricks_token = os.getenv('DATABRICKS_TOKEN')

if not databricks_host or not databricks_token:
    raise ValueError("Environment variables 'DATABRICKS_HOST' and 'DATABRICKS_TOKEN' must be set")

# Define the API endpoint for listing catalogs
url = f"{databricks_host}/api/2.1/unity-catalog/catalogs"

# Set up the headers for authentication
headers = {
    "Authorization": f"Bearer {databricks_token}",
    "Content-Type": "application/json"
}

# Make the request to list all catalogs
response = requests.get(url, headers=headers)

# Check for a successful response
if response.status_code != 200:
    raise Exception(f"Error fetching catalogs: {response.text}")

# Parse the JSON response
catalogs = response.json().get('catalogs', [])

# Print the catalogs
print("Available catalogs:")
for catalog in catalogs:
    print(catalog['name'])