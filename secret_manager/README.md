# GCP Secret Updater (Webhook)

This project provides a secure, generic REST API webhook to update secrets in Google Cloud Secret Manager. It acts as a bridge so local scripts (like an E*TRADE local auth flow) can update cloud secrets without needing GCP SDKs or IAM service account keys on the local machine.

## Architecture

The system is split into two distinct parts:
1. **The Server (Cloud Function)**: Runs on Google Cloud. It receives an HTTP POST request, authenticates it via a custom header, and uses your `gcp_parameter_manager.py` utility to update the Secret Manager.
2. **The Client (Local Helper)**: Runs on your local machine (e.g., Windows laptop). It simply sends the updated keys over the internet to the Cloud Function.

---

## File Breakdown

### Root Directory (The Cloud Server)
These files constitute the Google Cloud Function and are the only files deployed to GCP.

* **`main.py`**: The Cloud Function entry point. It receives the HTTP request, verifies the `X-API-Key` password, parses the JSON payload, and passes the data to the parameter manager utility.
* **`gcp_parameter_manager.py`**: Your custom GCP Secret Manager utility (downloaded from your GitHub). This contains the core logic for interacting with the GCP Secret Manager API. `main.py` imports this file.
* **`requirements.txt`**: The Python dependencies required by Google Cloud to run the function (e.g., `functions-framework`, `google-cloud-secret-manager`).
* **`deploy.sh`**: A convenience shell script to deploy the Cloud Function as a 2nd Gen function to your `nimesa-data` project under the designated service account.

### `local_client/` Directory (The Local Client)
This folder is purely for your local machine. It does **not** get executed by Google Cloud.

* **`update_secret_client.py`**: A simple Python wrapper script. It uses the `requests` library to format your data into JSON and sends it to the Cloud Function. You can copy/paste this code directly into your local E*TRADE python scripts.

---

## How to Deploy

1. Open `deploy.sh` and change `"your_strong_webhook_password"` to a strong, random string. This acts as the password to protect your webhook from unauthorized access.
2. Ensure you are authenticated with the Google Cloud CLI (`gcloud auth login`).
3. Run the deployment script from the root folder:
   ```bash
   ./deploy.sh
   ```

## How to Use (Client Side)

Once deployed, GCP will output a trigger URL (e.g., `https://us-central1-nimesa-data.cloudfunctions.net/generic-secret-updater`).

1. Open `local_client/update_secret_client.py`.
2. Update the `WEBHOOK_URL` variable with your actual deployed URL.
3. Update `WEBHOOK_SECRET` to match the password you set in `deploy.sh`.
4. Call the function in your local Python code:

```python
from update_secret_client import update_cloud_secret

# Example updating a JSON payload
update_cloud_secret(
    secret_id="etrade_api_tokens", 
    secret_value={
        "oauth_token": "new_token_123",
        "oauth_token_secret": "new_secret_456"
    }
)

# Example updating a simple string
update_cloud_secret(
    secret_id="openai_api_key",
    secret_value="sk-proj-..."
)
```
