# shared-infra/main.tf

provider "google" {
  project     = var.gcp_project_id
  region      = var.gke_region
}

resource "google_compute_network" "shared_vpc" {
  name                    = var.vpc_name
  auto_create_subnetworks  = false
}

resource "google_compute_subnetwork" "dev_subnet" {
  name          = "dev-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.gke_region
  network       = google_compute_network.shared_vpc.id
  private_ip_google_access = true
}

resource "google_compute_subnetwork" "qa_subnet" {
  name          = "qa-subnet"
  ip_cidr_range = "10.0.2.0/24"
  region        = var.gke_region
  network       = google_compute_network.shared_vpc.id
  private_ip_google_access = true
}

resource "google_compute_subnetwork" "prod_subnet" {
  name          = "prod-subnet"
  ip_cidr_range = "10.0.3.0/24"
  region        = var.gke_region
  network       = google_compute_network.shared_vpc.id
  private_ip_google_access = true
}

# Added firewall rules for GKE
resource "google_compute_firewall" "gke_firewall" {
  name    = "gke-firewall"
  network = google_compute_network.shared_vpc.id

  allow {
    protocol = "tcp"
    ports    = ["10250", "443", "80", "8080"] # Added ports
  }

  source_ranges = ["0.0.0.0/0"]
}
