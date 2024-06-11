from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core import Workspace
import os

def check_service_principal():
    try:
        # Fetching environment variables for the service principal credentials
        client_id = os.getenv("AZURE_CLIENT_ID")
        client_secret = os.getenv("AZURE_CLIENT_SECRET")
        tenant_id = os.getenv("AZURE_TENANT_ID")
        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")

        if not all([client_id, client_secret, tenant_id, subscription_id]):
            raise ValueError("One or more Azure Service Principal credentials are not set in environment variables.")

        # Authenticating using the service principal
        credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
        resource_client = ResourceManagementClient(credential, subscription_id)

        # Attempt to list resource groups as a basic check
        resource_groups = list(resource_client.resource_groups.list())
        
        print(f"Successfully authenticated and found {len(resource_groups)} resource groups.")

        svc_pr_password = os.environ.get("AZUREML_PASSWORD")

        svc_pr = ServicePrincipalAuthentication(
            tenant_id=tenant_id,
            service_principal_id=client_id,
            service_principal_password=client_secret)
        
        # ML Workspace Test
        ws = Workspace(subscription_id=subscription_id,
                resource_group="MLops_project",
                workspace_name="hamzaworkspace",
                auth=svc_pr
            )

        print(ws.name, ws.resource_group, ws.location, ws.subscription_id)

        return True

    except ClientAuthenticationError as auth_error:
        print(f"Authentication failed: {auth_error}")
    except HttpResponseError as http_error:
        print(f"HTTP request failed: {http_error}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return False

if __name__ == "__main__":
    if check_service_principal():
        print("Service Principal is working correctly.")
    else:
        print("Service Principal check failed.")
