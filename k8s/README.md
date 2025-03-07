Set up the GKE Autopilot cluster:
gcloud container clusters create dera-cluster \
 — project=dera \
 — region=us-central1 \
 — release-channel=autopilot \
 — enable-stackdriver-kubernetes

Set up Google Cloud & Secrets

1. Enable GKE & GCR

gcloud services list --enabled

gcloud services enable containerregistry.googleapis.com
gcloud services enable container.googleapis.com

gcloud iam service-accounts create github-actions-sa \
    --description="GitHub Actions GKE Deployment" \
    --display-name="GitHub Actions SA"

Attach permissions:


gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/container.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding <your-project-id> \
    --member="serviceAccount:github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com


kubectl create secret generic argocd-github-pat --from-literal=token=<your-github-pat> -n argocd


argocd repo add https://github.com/<your-username>/<your-repo> \
  --name github-repo \
  --password <your-github-pat> \
  --username <your-github-username> \
  --insecure-ignore-host-key
