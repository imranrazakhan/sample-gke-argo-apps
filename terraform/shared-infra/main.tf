# shared-infra/main.tf

provider "google" {
  credentials = file("<YOUR-CREDENTIALS-FILE>.json")
  project     = var.project_id
  region      = var.region
}

resource "google_compute_network" "shared_vpc" {
  name                    = "shared-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "dev_subnet" {
  name          = "dev-subnet"
  region        = var.region
  network       = google_compute_network.shared_vpc.id
  ip_cidr_range = "10.0.0.0/24"
}

resource "google_compute_subnetwork" "qa_subnet" {
  name          = "qa-subnet"
  region        = var.region
  network       = google_compute_network.shared_vpc.id
  ip_cidr_range = "10.0.1.0/24"
}

resource "google_compute_subnetwork" "prod_subnet" {
  name          = "prod-subnet"
  region        = var.region
  network       = google_compute_network.shared_vpc.id
  ip_cidr_range = "10.0.2.0/24"
}

resource "google_container_cluster" "gke_autopilot" {
  name     = "gke-autopilot-cluster"
  location = var.region

  # GKE Autopilot with private mode
  autopilot = true
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = true
  }

  network = google_compute_network.shared_vpc.id
  subnetwork = google_compute_subnetwork.dev_subnet.id # You can change for dev/qa/prod in separate workspaces
}

output "vpc_id" {
  value = google_compute_network.shared_vpc.id
}

output "dev_subnet_id" {
  value = google_compute_subnetwork.dev_subnet.id
}

output "qa_subnet_id" {
  value = google_compute_subnetwork.qa_subnet.id
}

output "prod_subnet_id" {
  value = google_compute_subnetwork.prod_subnet.id
}

output "gke_cluster_endpoint" {
  value = google_container_cluster.gke_autopilot.endpoint
}
