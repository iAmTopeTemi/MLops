import requests
import json, os
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
            workspace_name="temiworkspace",
            auth=svc_pr
    )

    # Get the deployed web service
    service_name = 'sim-rf-service'
    service = Webservice(workspace=ws, name=service_name)

    # Get the scoring URI
    scoring_uri = service.scoring_uri

    print("Scoring URI:", scoring_uri)

    # Set the headers for the request
    headers = {'Content-Type': 'application/json'}

    # Sample data to send to the model for prediction
    # data = {
    #     "data": [
    #         [5.1, 3.5, 1.4, 0.2],  # Example input data point
    #         [6.7, 3.0, 5.2, 2.3]   # Another example input data point
    #     ]
    # }
    data = [
        [5.1, 3.5, 1.4, 0.2],  # Example input data point
        [6.7, 3.0, 5.2, 2.3]   # Another example input data point
    ]

    # Convert the data to JSON format
    input_data = json.dumps(data)

    # Send the request to the model endpoint
    response = requests.post(scoring_uri, data=input_data, headers=headers)

    # Print the response from the model
    print("Testing Model Response: ", response.json())

except Exception as e:
    print("Failed! ", str(e))