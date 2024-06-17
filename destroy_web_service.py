import os
from azureml.core import Workspace, Webservice
from azureml.core.authentication import ServicePrincipalAuthentication

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

    # Get the web service
    service_name = 'sim-rf-service'  # Replace with your service name
    service = Webservice(workspace=ws, name=service_name)
    print("Service Logs:", service.get_logs())

    # Delete the web service
    service.delete()
    print(f"Service {service_name} deleted")
except Exception as e:
    print("Failed! ", str(e))