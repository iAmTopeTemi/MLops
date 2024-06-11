import os
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError

try:
    # Set up the Azure credentials
    tenant_id = os.getenv('AZURE_TENANT_ID')
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET')
    adls_account_name = 'storageaccountfortemi'

    # Authenticate using the service principal
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)

    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient(account_url=f"https://{adls_account_name}.blob.core.windows.net", credential=credential)

    # Specify the container and blob name
    container_name = 'demo-rf-models'
    blob_name = 'rf-model-challenger'

    # Get a ContainerClient
    container_client = blob_service_client.get_container_client(container_name)

    # Check if the container exists, if not, create it
    try:
        container_client.create_container()
        print(f"Container '{container_name}' created.")
    except ResourceExistsError:
        print(f"Container '{container_name}' already exists.")

    # Get a BlobClient
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Upload the model
    with open('demo_rf_model', 'rb') as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"Model saved to ADLS at {blob_client.url}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
