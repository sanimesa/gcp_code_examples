import os
import json
import logging
from google.cloud import secretmanager
import functions_framework

# Initialize GCP Secret Manager Client
secret_client = secretmanager.SecretManagerServiceClient()

# Configuration from Environment Variables
PROJECT_ID = os.environ.get("GCP_PROJECT")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")  # Protects this endpoint!

@functions_framework.http
def update_gcp_secret(request):
    """Generic HTTP Cloud Function to update any secret in GCP Secret Manager."""
    try:
        # 1. Security check: require a custom header
        auth_header = request.headers.get("X-API-Key")
        if not auth_header or auth_header != WEBHOOK_SECRET:
            return ({"error": "Unauthorized"}, 403)

        # 2. Parse the incoming JSON payload
        request_json = request.get_json(silent=True)
        if not request_json:
             return ({"error": "Invalid JSON"}, 400)
             
        secret_id = request_json.get("secret_id")
        secret_value = request_json.get("secret_value")

        if not secret_id or not secret_value:
            return ({"error": "Missing required fields: 'secret_id' and 'secret_value'"}, 400)

        # If the value passed is a dictionary or list, convert it to a JSON string
        if isinstance(secret_value, (dict, list)):
            payload_string = json.dumps(secret_value)
        else:
            payload_string = str(secret_value)

        # 3. Add a new version to the Secret Manager
        if not PROJECT_ID:
            return ({"error": "GCP_PROJECT environment variable is missing"}, 500)
            
        parent = f"projects/{PROJECT_ID}/secrets/{secret_id}"
        
        response = secret_client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": payload_string.encode("UTF-8")},
            }
        )

        return ({"status": "success", "message": f"Secret '{secret_id}' updated. New version: {response.name}"}, 200)

    except Exception as e:
        logging.error(f"Function error: {e}")
        return ({"error": str(e)}, 500)
