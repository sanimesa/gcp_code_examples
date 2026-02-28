import os
import json
import logging
import functions_framework
from gcp_parameter_manager import ParameterManager

# Configuration from Environment Variables
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")  # Protects this endpoint!
# Default to GOOGLE_CLOUD_PROJECT (standard for GCP) or fallback to GCP_PROJECT
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")

@functions_framework.http
def update_gcp_secret(request):
    """Generic HTTP Cloud Function to update any secret using the custom ParameterManager utility."""
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

        # 3. Use the custom ParameterManager to update the secret
        if not PROJECT_ID:
            return ({"error": "GOOGLE_CLOUD_PROJECT environment variable is missing"}, 500)
            
        success = ParameterManager.update_parameter(
            secret_id=secret_id, 
            payload=payload_string, 
            project_id=PROJECT_ID
        )

        if success:
            return ({"status": "success", "message": f"Secret '{secret_id}' updated successfully."}, 200)
        else:
            return ({"error": f"Failed to update secret '{secret_id}'. Check Cloud Function logs."}, 500)

    except Exception as e:
        logging.error(f"Function error: {e}")
        return ({"error": str(e)}, 500)
