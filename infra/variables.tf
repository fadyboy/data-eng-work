variable "bq_dataset" {
  description = "Big query dataset name"
  default = "datatalks_dataset"
}

variable "gcs_bucket" {
    description = "Gcs bucket name"
    default = "sodium-chalice-412103-bucket"
}

variable "location" {   
    description = "Project location"
    default = "US"
}