variable "gcp_project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "gke_region" {
  description = "The GCP region"
  type        = string
  default     = "us-central1"
}
