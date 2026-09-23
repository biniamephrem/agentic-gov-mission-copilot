output "evidence_bucket" {
  value = google_storage_bucket.evidence.name
}

output "kms_key_name" {
  value = google_kms_crypto_key.main.name
}
