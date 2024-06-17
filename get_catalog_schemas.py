# import os
# import requests

# # Ensure environment variables are set correctly
# os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
# os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')
# databricks_host = os.getenv('DATABRICKS_HOST')
# databricks_token = os.getenv('DATABRICKS_TOKEN')

# if not databricks_host or not databricks_token:
#     raise ValueError("Environment variables 'DATABRICKS_HOST' and 'DATABRICKS_TOKEN' must be set")

# # Specify the catalog name
# catalog_name = 'hamzauc'

# # Construct the API endpoint URL
# url = f"{databricks_host}/api/2.1/unity-catalog/catalogs/{catalog_name}/schemas"

# # Set up the headers for authentication
# headers = {
#     "Authorization": f"Bearer {databricks_token}",
#     "Content-Type": "application/json"
# }

# try:
#     # Make the request to list all schemas in the specified catalog
#     response = requests.get(url, headers=headers, timeout=10)
    
#     # Check for a successful response
#     response.raise_for_status()
    
#     # Parse the JSON response
#     schemas = response.json().get('schemas', [])

#     # Print the schemas
#     print(f"Schemas in catalog '{catalog_name}':")
#     for schema in schemas:
#         print(f"Name: {schema['name']}, ID: {schema['id']}")
# except requests.exceptions.RequestException as e:
#     print(f"An error occurred: {e}")
import os
import requests

# Ensure environment variables are set correctly
os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')
databricks_host = os.getenv('DATABRICKS_HOST')
databricks_token = os.getenv('DATABRICKS_TOKEN')

if not databricks_host or not databricks_token:
    raise ValueError("Environment variables 'DATABRICKS_HOST' and 'DATABRICKS_TOKEN' must be set")

# Specify the catalog name
catalog_name = 'hamzauc'

# Construct the API endpoint URL for listing schemas
url = f"{databricks_host}/api/2.1/unity-catalog/schemas"

# Set up the headers for authentication
headers = {
    "Authorization": f"Bearer {databricks_token}",
    "Content-Type": "application/json"
}

# Include the catalog name in the query parameters
params = {
    "catalog_name": catalog_name
}

try:
    # Make the request to list all schemas in the specified catalog
    response = requests.get(url, headers=headers, params=params, timeout=10)
    
    # Check for a successful response
    response.raise_for_status()
    
    # Parse the JSON response
    schemas = response.json().get('schemas', [])

    # Print the schemas
    print(f"Schemas in catalog '{catalog_name}':")
    for schema in schemas:
        schema_name = schema['name']
        print(f"Schema: {schema}")
        
        # Fetch tables (potential models) within the schema
        tables_url = f"{databricks_host}/api/2.1/unity-catalog/tables"
        tables_params = {
            "catalog_name": catalog_name,
            "schema_name": schema_name
        }
        
        tables_response = requests.get(tables_url, headers=headers, params=tables_params, timeout=10)
        tables = tables_response.json().get('tables', [])
        
        # Print the tables (potential models)
        print(f"Tables in schema '{schema_name}':")
        for table in tables:
            print(f"Table: {table}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")