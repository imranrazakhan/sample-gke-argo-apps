# dev/main.tf

provider "google" {
  credentials = file("<YOUR-CREDENTIALS-FILE>.json")
  project     = var.project_id
  region      = var.region
}

# Reference the outputs from the shared-infra workspace
data "terraform_remote_state" "shared_infra" {
  backend = "remote"

  config = {
    organization = "your-org"
    workspaces = {
      name = "shared-infra"
    }
  }
}

resource "google_container_cluster" "gke_autopilot_dev" {
  name     = "gke-autopilot-cluster-dev"
  location = var.region

  # GKE Autopilot with private mode
  autopilot = true
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = true
  }

  network    = data.terraform_remote_state.shared_infra.outputs["vpc_id"]
  subnetwork = data.terraform_remote_state.shared_infra.outputs["dev_subnet_id"]
}

output "dev_gke_cluster_endpoint" {
  value = google_container_cluster.gke_autopilot_dev.endpoint
}
