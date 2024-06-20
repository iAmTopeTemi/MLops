from azureml.core import Workspace, Model, Environment
from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.exceptions import WebserviceException
import os
import mlflow

# Set MLflow tracking URI
mlflow.set_tracking_uri("databricks")
mlflow.set_registry_uri('databricks-uc')
os.environ['DATABRICKS_HOST'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['DATABRICKS_TOKEN'] = os.getenv('DATABRICKS_TOKEN')

# Initialize the MLflow client
client = mlflow.tracking.MlflowClient()

def retrieve_latest_champion_model_from_unity_catalog():
    # Retrieve the model version associated with the run ID
    # Correct the model name format
    catalog_name = "temiuc"
    schema_name = "default"
    model_name = f"{catalog_name}.{schema_name}.sim_rf_model_prod"
    latest_model = None

    # Retrieve the latest model version with alias "Champion"
    latest_version_info = client.get_model_version_by_alias(model_name, "Champion")
    print(f"Latest model version with alias 'Champion': {latest_version_info.version}")

    # Load the latest model version
    model_uri = f"models:/{model_name}@Champion"
    os.makedirs("./sim_rf_model_prod", exist_ok=True)
    latest_model = mlflow.pyfunc.load_model(model_uri, dst_path="./sim_rf_model_prod")
    print(f"Loaded model URI: {model_uri}")
    return model_uri

def deploy_model_to_workspace(model_uri):
    try:
        client_id = os.getenv("AZURE_CLIENT_ID")
        client_secret = os.getenv("AZURE_CLIENT_SECRET")
        tenant_id = os.getenv("AZURE_TENANT_ID")
        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

        # Connect to workspace
        svc_pr = ServicePrincipalAuthentication(
            tenant_id=tenant_id,
            service_principal_id=client_id,
            service_principal_password=client_secret
        )

        # ML Workspace Test
        ws = Workspace(subscription_id=subscription_id,
                resource_group="MLops_project",
                workspace_name="temiworkspace",
                auth=svc_pr
        )

        model_path = './sim_rf_model_prod/artifacts/sim_rf_model_prod_adls/model.pkl'

        # Registering the model
        model = Model.register(workspace=ws,
            model_name='sim_rf_model_prod',
            model_path=model_path
            # model_path=model_uri
        )

        # Defining inference configuration
        env = Environment.from_conda_specification(name='.menv', file_path='main_prod_branch/environment.yml')
        inference_config = InferenceConfig(entry_script='main_prod_branch/score.py', environment=env)

        # Define deployment configuration
        aci_config = AciWebservice.deploy_configuration(
            cpu_cores=1,
            memory_gb=1,
            enable_app_insights=True,  # Enable application insights for detailed logging
            collect_model_data=True,   # Collect model data for detailed logging
        )

        # Deploy the model
        service = Model.deploy(workspace=ws,
            name='sim-rf-service-prod',
            models=[model],
            inference_config=inference_config,
            deployment_config=aci_config
        )

        service.wait_for_deployment(show_output=True)
        print(service.scoring_uri)
    except Exception as e:
        print("Failed! ", str(e))

model_uri = retrieve_latest_champion_model_from_unity_catalog()
deploy_model_to_workspace(model_uri)