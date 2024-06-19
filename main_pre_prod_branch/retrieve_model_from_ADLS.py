import os
import shutil
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential

# Azure ADLS credentials and details
tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
adls_account_name = "mlopstemilocaldev"
file_system_name = "models"
directory_name = "challenger_models/sim_rf_model"  # The directory in ADLS where the model is saved
local_directory_path = "./sim_rf_model_pre_prod_adls"  # Local path to save the downloaded model

# Function to download files from ADLS to a local directory
def download_directory_from_adls(adls_directory_path, local_directory_path, file_system_client):
    # Ensure the local directory is clean
    if os.path.exists(local_directory_path):
        shutil.rmtree(local_directory_path)
    os.makedirs(local_directory_path, exist_ok=True)
    paths = file_system_client.get_paths(path=adls_directory_path)
    
    for path in paths:
        if not path.is_directory:
            local_file_path = os.path.join(local_directory_path, os.path.relpath(path.name, adls_directory_path))
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            file_client = file_system_client.get_file_client(path.name)

            download = file_client.download_file()
            file_content = download.readall()
            file_size = len(file_content)
            
            with open(local_file_path, "wb") as local_file:
                local_file.write(file_content)
                print(f"Downloaded: {local_file_path} (Size: {file_size} bytes)")
                
            if file_size == 0:
                print(f"Warning: Downloaded file {local_file_path} is empty.")
            
            # with open(local_file_path, "wb") as local_file:
            #     download = file_client.download_file()
            #     local_file.write(download.readall())
            #     print(f"Downloaded: {local_file_path}")

# Authenticate to ADLS using Service Principal
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
adls_service_client = DataLakeServiceClient(account_url=f"https://{adls_account_name}.dfs.core.windows.net", credential=credential)
file_system_client = adls_service_client.get_file_system_client(file_system=file_system_name)

# Download the directory from ADLS to local
download_directory_from_adls(directory_name, local_directory_path, file_system_client)

print(f"Model directory downloaded from ADLS to local directory: {local_directory_path}")



# import shutil
# import os
# from azureml.core import Workspace, Model, Environment
# from azureml.core.webservice import AciWebservice
# from azureml.core.model import InferenceConfig
# from azureml.core.authentication import ServicePrincipalAuthentication
# from azureml.exceptions import WebserviceException
# import os
# import mlflow

# # Set MLflow tracking URI
# mlflow.set_tracking_uri("databricks")
# mlflow.set_registry_uri('databricks-uc')
# os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
# os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')

# # Initialize the MLflow client
# client = mlflow.tracking.MlflowClient()

# def retrieve_latest_challenger_model_from_unity_catalog():
#     # Retrieve the model version associated with the run ID
#     # Correct the model name format
#     catalog_name = "temiuc"
#     schema_name = "default"
#     model_name = f"{catalog_name}.{schema_name}.sim_rf_model"
#     latest_model = None

#     # Retrieve the latest model version with alias "Challenger-pre-test"
#     latest_version_info = client.get_model_version_by_alias(model_name, "Challenger")
#     print(f"Latest model version with alias 'Challenger': {latest_version_info.version}")

#     # Load the latest model version
#     model_uri = f"models:/{model_name}@Challenger"
#     os.makedirs("./sim_rf_model_pre_prod_adls", exist_ok=True)
#     latest_model = mlflow.pyfunc.load_model(model_uri, dst_path="./sim_rf_model_pre_prod_adls")
#     print(f"Loaded model URI: {model_uri}")
#     return model_uri

# def copy_folder(src_folder, dest_folder):
#     """
#     Copies the src_folder to dest_folder.
    
#     :param src_folder: str, path to the source folder
#     :param dest_folder: str, path to the destination folder
#     """
#     # Check if the source folder exists
#     if not os.path.exists(src_folder):
#         print(f"Source folder '{src_folder}' does not exist.")
#         return

#     # Check if the destination folder already exists
#     if os.path.exists(dest_folder):
#         print(f"Destination folder '{dest_folder}' already exists.")
#         return
    
#     # Copy the source folder to the destination folder
#     shutil.copytree(src_folder, dest_folder)
#     print(f"Copied '{src_folder}' to '{dest_folder}' successfully.")

# # Example usage
# source_folder = "./sim_rf_model"
# destination_folder = "./sim_rf_model_pre_prod_adls"

# copy_folder(source_folder, destination_folder)
# model_uri = retrieve_latest_challenger_model_from_unity_catalog()