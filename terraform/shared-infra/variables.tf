# shared-infra/variables.tf

variable "gcp_project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "your-default-project-id"
}

variable "gke_region" {
  description = "The GCP region"
  type        = string
  default     = "us-central1"
}

variable "vpc_name" {
  description = "Name of the shared VPC"
  type        = string
  default     = "shared-vpc"
}
