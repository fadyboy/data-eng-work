variable "bq_dataset" {
  description = "Big query dataset name"
  default     = "datatalks_dataset"
}

variable "gcs_bucket" {
  description = "Gcs bucket name"
  default     = "sodium-chalice-412103-bucket"
}

variable "location" {
  description = "Project location"
  default     = "US"
}

variable "project_id" {
  description = "default google cloud project id"
  default     = "sodium-chalice-412103"
}

variable "region" {
  description = "default google cloud region"
  default     = "us-central1"
}

variable "repository" {
  type        = string
  description = "The name of the Artifact Registry repository to be created"
  default     = "mage-data-prep"
}

variable "database_user" {
  type        = string
  description = "The username of the Postgres database."
  default     = "mageuser"
}

variable "database_password" {
  type        = string
  description = "The password of the Postgres database."
  sensitive   = true
}

variable "docker_image" {
  type        = string
  description = "The docker image to deploy to Cloud Run."
  default     = "mageai/mageai:latest"
}

variable "domain" {
  description = "Domain name to run the load balancer on. Used if `ssl` is `true`."
  type        = string
  default     = ""
}

variable "ssl" {
  description = "Run load balancer on HTTPS and provision managed certificate with provided `domain`."
  type        = bool
  default     = false
}

variable "app_name" {
  type        = string
  description = "Application Name"
  default     = "mage-data-prep"
}

variable "container_cpu" {
  description = "Container cpu"
  default     = "2000m"
}

variable "container_memory" {
  description = "Container memory"
  default     = "2G"
}