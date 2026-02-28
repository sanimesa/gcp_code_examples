import requests
import json

def update_cloud_secret(secret_id, secret_value):
    """
    Cloud-agnostic generic way to push new secrets via REST API.
    Works for any secret ID and value (dict, list, string).
    """
    # Replace with the URL of your new updater Cloud Function
    WEBHOOK_URL = "https://REGION-YOUR_PROJECT_ID.cloudfunctions.net/generic-secret-updater"
    
    # Replace with the strong, random password set in the Cloud Function environment
    WEBHOOK_SECRET = "super_secret_updater_key_123" 

    payload = {
        "secret_id": secret_id,
        "secret_value": secret_value
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": WEBHOOK_SECRET  # Important security measure
    }

    print(f"[*] Pushing new value for secret '{secret_id}' to the cloud...")
    response = requests.post(WEBHOOK_URL, json=payload, headers=headers)

    if response.status_code == 200:
        print(f"[+] Success! {response.json()}")
    else:
        print(f"[-] Failed to push token. Status: {response.status_code}, Response: {response.text}")

# --- Example Usage for E*TRADE ---
#
# update_cloud_secret(
#     secret_id="etrade_api_tokens", 
#     secret_value={
#         "oauth_token": "new_oauth_tk_123",
#         "oauth_token_secret": "new_oauth_sec_456"
#     }
# )
#
# --- Example Usage for something else ---
#
# update_cloud_secret(
#     secret_id="openai_api_key",
#     secret_value="sk-proj-some-long-string..."
# )
