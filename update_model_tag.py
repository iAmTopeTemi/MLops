import mlflow
import os

# Set MLflow tracking URI
mlflow.set_tracking_uri("databricks")
os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')

# Get the run ID from the environment variable
run_id = os.getenv('MLFLOW_RUN_ID')
if not run_id:
    raise ValueError("Run ID environment variable 'MLFLOW_RUN_ID' is not set or is null")

# Initialize the MLflow client
client = mlflow.tracking.MlflowClient()

# Retrieve the model version associated with the run ID
model_name = 'demo_rf_model'
latest_model = None

for mv in client.search_model_versions(f"name='{model_name}'"):
    if mv.run_id == run_id:
        latest_model = mv
        break

if not latest_model:
    raise ValueError(f"No model version found for run ID: {run_id}")

# Update the model tag
client.set_model_version_tag(
    name=model_name,
    version=latest_model.version,
    key="stage",
    value="development"
)

print(f"Updated model version {latest_model.version} tag to 'Challenger'")