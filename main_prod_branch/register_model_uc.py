import os
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from mlflow.exceptions import RestException

print("MLFLOW_TRACKING_URI:", os.getenv('MLFLOW_TRACKING_URI'))
print("MLFLOW_RUN_ID:", os.getenv('MLFLOW_RUN_ID'))
print("DATABRICKS_TOKEN:", os.getenv('DATABRICKS_TOKEN'))
os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')
# Configure MLflow
mlflow.set_tracking_uri("databricks")
mlflow.set_registry_uri('databricks-uc')

run_id = os.getenv('MLFLOW_RUN_ID')

# Initialize the MLflow client
client = MlflowClient()

# Define the catalog and schema names
catalog_name = "temiuc"
schema_name = "default"
model_name = f"{catalog_name}.{schema_name}.sim_rf_model_prod"

# Register the model
model_uri = f"runs:/{run_id}/sim_rf_model_prod"
try:
    registered_model = client.create_registered_model(model_name)
    print(f"Registered new model with name: {model_name}")
except RestException as e:
    if e.error_code == "RESOURCE_ALREADY_EXISTS":
        print(f"Model {model_name} already exists. Creating a new version.")
    else:
        raise e

# Create a new model version
model_version = client.create_model_version(model_name, model_uri, run_id)
client.set_registered_model_alias(model_name, "Champion", model_version.version)

print(f"Model registered with name: {model_name}, version: {model_version.version}")