#!/bin/bash
gcloud functions deploy generic-secret-updater \
  --gen2 \
  --region us-central1 \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point update_gcp_secret \
  --service-account function-updater@nimesa-data.iam.gserviceaccount.com \
  --set-env-vars GOOGLE_CLOUD_PROJECT="nimesa-data",GCP_PROJECT="nimesa-data",WEBHOOK_SECRET="your_strong_webhook_password"
