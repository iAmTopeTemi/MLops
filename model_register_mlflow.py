import os
import mlflow

# Configure MLflow
mlflow.set_tracking_uri("databricks")
model_name = "demo_rf_model"
os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')

# Retrieve the run ID from an environment variable or Jenkins parameter
run_id = os.getenv('MLFLOW_RUN_ID')
model_uri = f"runs:/{run_id}/{model_name}"
print(f"Retrieved RUN ID from environment variable: {run_id}")  # Debugging line

if run_id is None or run_id == 'null':
    raise ValueError("Run ID environment variable 'MLFLOW_RUN_ID' is not set or is null")

# Register the model
mv = mlflow.register_model(model_uri=model_uri, name=model_name, tags={"stage": "development"})

# Assign "Challenger" alias to the registered model
# client = mlflow.tracking.MlflowClient()
# client.set_registered_model_alias(mv.name, "Challenger", mv.version)
# mlflow.exceptions.MlflowException: Method 'set_registered_model_alias' is unsupported for models in the Workspace Model Registry.
# Upgrade to Models in Unity Catalog to access the latest features.
# You can configure the MLflow Python client to access models in Unity Catalog by running mlflow.set_registry_uri('databricks-uc') before accessing models.
