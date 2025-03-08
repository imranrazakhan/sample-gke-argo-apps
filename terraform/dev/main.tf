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

  enable_autopilot = true
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block = "172.16.0.32/28"
  }

  network    = data.terraform_remote_state.shared_infra.outputs["vpc_id"]
  subnetwork = data.terraform_remote_state.shared_infra.outputs.subnet_ids[0]

  # Disable deletion protection
  deletion_protection = false
}
