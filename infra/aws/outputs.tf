output "evidence_bucket" {
  value = aws_s3_bucket.evidence.bucket
}

output "mission_state_table" {
  value = aws_dynamodb_table.mission_state.name
}

output "log_group" {
  value = aws_cloudwatch_log_group.app.name
}
