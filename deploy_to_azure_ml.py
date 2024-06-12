from azureml.core import Workspace, Model, Environment
from azureml.core.webservice import AciWebservice, Webservice
from azureml.core.model import InferenceConfig
from azureml.core.authentication import ServicePrincipalAuthentication
import joblib
import os

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
            workspace_name="hamzaworkspace",
            auth=svc_pr
    )

    model_path = './demo_rf_model'

    # Registering the model
    model = Model.register(workspace=ws,
        model_name='demo_rf_model',
        model_path=model_path
    )

    # Defining inference configuration
    env = Environment.from_conda_specification(name='.menv', file_path='environment.yml')
    inference_config = InferenceConfig(entry_script='score.py', environment=env)

    # Define deployment configuration
    aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

    # Deploy the model
    service = Model.deploy(workspace=ws,
        name='demo-rf-service',
        models=[model],
        inference_config=inference_config,
        deployment_config=aci_config
    )

    service.wait_for_deployment(show_output=True)
    print(service.scoring_uri)
except Exception as e:
    print("Failed! ", str(e))