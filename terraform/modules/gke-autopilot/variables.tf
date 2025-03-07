variable "env" {
  description = "Environment name (dev/qa/prod)"
  type        = string
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "subnet_cidr" {
  description = "CIDR range for the primary subnet"
  type        = string
}

variable "pod_cidr" {
  description = "CIDR range for GKE pods"
  type        = string
}

variable "service_cidr" {
  description = "CIDR range for GKE services"
  type        = string
}

variable "master_cidr" {
  description = "CIDR range for the GKE control plane"
  type        = string
}
