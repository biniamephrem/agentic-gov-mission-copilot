terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

resource "aws_kms_key" "app" {
  description             = "KMS key for agentic mission copilot demo"
  deletion_window_in_days = 7
  enable_key_rotation     = true
}

resource "aws_s3_bucket" "evidence" {
  bucket_prefix = "${var.name}-evidence-"
}

resource "aws_s3_bucket_public_access_block" "evidence" {
  bucket                  = aws_s3_bucket.evidence.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "evidence" {
  bucket = aws_s3_bucket.evidence.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.app.arn
    }
  }
}

resource "aws_dynamodb_table" "mission_state" {
  name         = "${var.name}-mission-state"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "mission_id"

  attribute {
    name = "mission_id"
    type = "S"
  }

  server_side_encryption {
    enabled     = true
    kms_key_arn = aws_kms_key.app.arn
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_cloudwatch_log_group" "app" {
  name              = "/gov-agent/${var.name}"
  retention_in_days = 365
  kms_key_id        = aws_kms_key.app.arn
}

# Production expansion points:
# - VPC with private subnets and VPC endpoints
# - ECS/Fargate or EKS service running the API/orchestrator
# - Bedrock VPC endpoint / approved model endpoint
# - OpenSearch Serverless or Aurora PostgreSQL + pgvector
# - WAF / private ALB / API Gateway as mission boundary requires
# - IAM roles separated for inference, retrieval, and tool execution
# - CloudTrail, Security Hub, GuardDuty, Config, and SIEM integration
