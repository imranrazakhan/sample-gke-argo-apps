# dev/main.tf
provider "google" {
  project     = var.gcp_project_id
  region      = var.gke_region
}

# Reference the outputs from the shared-infra workspace
data "terraform_remote_state" "shared_infra" {
  backend = "remote"

  config = {
    organization = "dera"
    workspaces = {
      name = "shared-infra"
    }
  }
}

resource "google_container_cluster" "gke_autopilot_dev" {
  name     = "gke-autopilot-cluster-dev"
  location = var.gke_region

  # GKE Autopilot with private mode
  autopilot = true
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = true
  }

  network    = data.terraform_remote_state.shared_infra.outputs["vpc_id"]
  subnetwork = data.terraform_remote_state.shared_infra.outputs.subnet_ids[0]
}
