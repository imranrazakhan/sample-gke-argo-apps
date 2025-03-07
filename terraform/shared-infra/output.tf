# shared-infra/outputs.tf

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
