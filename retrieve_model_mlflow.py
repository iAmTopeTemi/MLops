import mlflow
import os, shutil

# Set MLflow tracking URI and experiment
mlflow.set_tracking_uri("databricks")
os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')

# Search for the latest model with tag "stage" = "development"
model_name = 'demo_rf_model'
latest_model = None

client = mlflow.tracking.MlflowClient()
for mv in client.search_model_versions(f"name='{model_name}'"):
    if dict(mv.tags).get("stage") == "Challenger":
        if latest_model is None or int(mv.version) > int(latest_model.version):
            latest_model = mv

if latest_model is None:
    raise Exception("No development stage model found.")

run_id = latest_model.run_id
print(run_id)

# Download the model
model_uri = f"runs:/{run_id}/{model_name}"
# local_model_path = f"./downloaded_model_{run_id}"
local_model_path = f"./{model_name}"

if os.path.exists(local_model_path):
    os.remove(local_model_path)

mlflow.artifacts.download_artifacts(model_uri, dst_path=local_model_path)

# print(f"Model downloaded to: {local_model_path}")
