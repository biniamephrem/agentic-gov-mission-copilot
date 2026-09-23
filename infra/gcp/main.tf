terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "evidence" {
  name                        = "${var.project_id}-agentic-gov-evidence"
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}

resource "google_firestore_database" "mission_state" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.firestore_location
  type        = "FIRESTORE_NATIVE"
}

resource "google_kms_key_ring" "main" {
  name     = "${var.name}-keyring"
  location = var.region
}

resource "google_kms_crypto_key" "main" {
  name            = "${var.name}-key"
  key_ring        = google_kms_key_ring.main.id
  rotation_period = "7776000s"
}

# Production expansion points:
# - Vertex AI Gemini model endpoint
# - Vertex AI Vector Search
# - Cloud Run or GKE
# - Secret Manager
# - Private Service Connect / VPC controls
# - Cloud Logging / Cloud Monitoring / Security Command Center
