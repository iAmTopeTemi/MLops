import mlflow
import os

# Set MLflow tracking URI
mlflow.set_tracking_uri("databricks")
mlflow.set_registry_uri('databricks-uc')
os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')

# Initialize the MLflow client
client = mlflow.tracking.MlflowClient()

# Retrieve the model version associated with the run ID
# Correct the model name format
catalog_name = "temiuc"
schema_name = "default"
model_name = f"{catalog_name}.{schema_name}.sim_rf_model"
latest_model = None

# Retrieve the latest model version with alias "Development"
latest_version_info = client.get_model_version_by_alias(model_name, "Development")
print(f"Latest model version with alias 'Development': {latest_version_info.version}")

# Load the latest model version
model_uri = f"models:/{model_name}@Development"
# latest_model = mlflow.pyfunc.load_model(model_uri)
print(f"Loaded model URI: {model_uri}")

client.set_registered_model_alias(model_name, "Challenger", latest_version_info.version)
print(f"Updated model alias to 'Challenger' for version: {latest_version_info.version}")