# shared-infra/outputs.tf

output "vpc_id" {
  value       = google_compute_network.shared_vpc.id
  description = "The ID of the shared VPC"
}

output "subnet_ids" {
  value       = [google_compute_subnetwork.dev_subnet.id, google_compute_subnetwork.qa_subnet.id, google_compute_subnetwork.prod_subnet.id]
  description = "List of subnet IDs"
}

output "subnet_names" {
  value = [google_compute_subnetwork.dev_subnet.name, google_compute_subnetwork.qa_subnet.name, google_compute_subnetwork.prod_subnet.name]
  description = "List of subnet names"
}
