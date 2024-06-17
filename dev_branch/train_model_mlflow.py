import os
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature
from mlflow.exceptions import RestException

print("MLFLOW_TRACKING_URI:", os.getenv('MLFLOW_TRACKING_URI'))
print("MLFLOW_RUN_ID:", os.getenv('MLFLOW_RUN_ID'))
print("DATABRICKS_TOKEN:", os.getenv('DATABRICKS_TOKEN'))
os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')
# Configure MLflow
mlflow.set_tracking_uri("databricks")
mlflow.set_experiment("/Shared/expsrfmodel1")


# Train a sample model
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Infer the model signature
signature = infer_signature(X_train, model.predict(X_train))

# Log model to MLflow
with mlflow.start_run() as run:
    mlflow.sklearn.log_model(model, "sim_rf_model", signature=signature)
    # print(f"HERE: {run.info}")
    run_id = run.info.run_id
    print(f"{run_id}")

mlflow.set_registry_uri('databricks-uc')
# Initialize the MLflow client
client = MlflowClient()

# Define the catalog and schema names
catalog_name = "temiuc"
schema_name = "default"
model_name = f"{catalog_name}.{schema_name}.sim_rf_model"

# Register the model
model_uri = f"runs:/{run_id}/sim_rf_model"
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
client.set_registered_model_alias(model_name, "Development", model_version.version)

print(f"Model registered with name: {model_name}, version: {model_version.version}")