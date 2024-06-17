import mlflow
import os
import mlflow.pyfunc
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from mlflow.models.signature import infer_signature

class CustomModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        model_path = context.artifacts["model"]
        model_file_path = os.path.join(model_path, "model.pkl")
        self.model = joblib.load(model_file_path)
        # self.model = joblib.load(context.artifacts["model"])

    def predict(self, context, model_input):
        return self.model.predict(model_input)

os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')

# Configure MLflow
mlflow.set_tracking_uri("databricks")
mlflow.set_experiment("/Shared/expsrfmodelpreprod")

# Path to the local model directory
local_model_path = "./sim_rf_model_pre_prod_adls"
model_file_path = os.path.join(local_model_path, "model.pkl")
# print("ls: ", os.listdir(local_model_path))
if not os.path.exists(model_file_path):
    raise FileNotFoundError(f"The model file {model_file_path} does not exist.")

# Load the existing model
# Load the existing model
try:
    model = joblib.load(model_file_path)
except Exception as e:
    print(f"Failed to load the model: {e}")
    raise
# model = joblib.load(os.path.join(local_model_path, "model.pkl"))

# Load sample data to infer the signature
iris = load_iris()
X_train, _, _, _ = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)

# Infer the model signature
input_example = X_train[:5]
signature = infer_signature(X_train, model.predict(X_train))

# Function to log the local model to MLflow
def log_local_model_to_mlflow(local_model_path):
    with mlflow.start_run() as run:
        # Log the model located at the local_model_path
        mlflow.pyfunc.log_model(
            artifact_path="sim_rf_model_pre_prod",
            python_model=CustomModel(),
            artifacts={"model": local_model_path},
            signature=signature,
            input_example=input_example
        )
        
        # Optional: log additional information or parameters if needed
        mlflow.log_param("model_stage", "pre_prod_pre_test")
        
        # Retrieve the run ID and the model URI
        run_id = run.info.run_id
        model_uri = f"runs:/{run_id}/sim_rf_model_pre_prod"
        
    # print(f"Model logged to MLflow with run ID: {run_id}")
    # print(f"Model URI: {model_uri}")
    return run_id, model_uri

# Log the model
run_id, model_uri = log_local_model_to_mlflow(local_model_path)
print(run_id)