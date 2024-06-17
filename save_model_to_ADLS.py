import os
import mlflow
import mlflow.sklearn
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential

# Azure ADLS credentials and details
tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
adls_account_name = "mlopstemilocaldev"
file_system_name = "models"
directory_name = "challenger_models/sim_rf_model"  # The directory in ADLS where you want to save the model
local_model_path = "./sim_rf_model"  # Local path where the model is downloaded

# Function to upload a local directory to ADLS
def upload_directory_to_adls(local_directory_path, adls_directory_path, file_system_client):
    for root, dirs, files in os.walk(local_directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            blob_path = os.path.relpath(file_path, local_directory_path)
            adls_blob_path = os.path.join(adls_directory_path, blob_path)
            
            with open(file_path, "rb") as data:
                file_client = file_system_client.get_file_client(adls_blob_path)
                file_client.create_file()
                file_content = data.read()
                file_client.append_data(file_content, offset=0, length=len(file_content))
                file_client.flush_data(len(file_content))
                print(f"Uploaded: {file_path} to {adls_blob_path} (Size: {len(file_content)} bytes)")
            # with open(file_path, "rb") as data:
            #     file_client = file_system_client.get_file_client(adls_blob_path)
            #     file_client.create_file()
            #     file_client.append_data(data, 0)
            #     file_client.flush_data(len(data.read()))

# Function to create a container if it doesn't exist
def create_container_if_not_exists(service_client, container_name):
    try:
        container_client = service_client.get_file_system_client(container_name)
        container_client.get_file_system_properties()
    except:
        service_client.create_file_system(file_system=container_name)
        print(f"Container '{container_name}' created.")

# Function to create a directory if it doesn't exist
def create_directory_if_not_exists(file_system_client, directory_name):
    directory_client = file_system_client.get_directory_client(directory_name)
    try:
        directory_client.get_directory_properties()
    except:
        directory_client.create_directory()
        print(f"Directory '{directory_name}' created.")

# Step 3: Authenticate to ADLS using Service Principal
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
adls_service_client = DataLakeServiceClient(account_url=f"https://{adls_account_name}.dfs.core.windows.net", credential=credential)

# Step 4: Create container if it doesn't exist
create_container_if_not_exists(adls_service_client, file_system_name)

# Step 5: Create directory if it doesn't exist
file_system_client = adls_service_client.get_file_system_client(file_system=file_system_name)
create_directory_if_not_exists(file_system_client, directory_name)

# Step 6: Upload the local model directory to ADLS
upload_directory_to_adls(local_model_path, directory_name, file_system_client)

print(f"Model uploaded to ADLS at directory: {directory_name}")