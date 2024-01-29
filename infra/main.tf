terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  # Configuration options
  project = "sodium-chalice-412103"
  region  = "us-central1"
}

resource "google_storage_bucket" "de-project" {
  name          = var.gcs_bucket
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "datalks-dataset" {
  dataset_id  = var.bq_dataset
  description = "sample bigquery dataset"
}