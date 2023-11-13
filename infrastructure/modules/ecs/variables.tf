variable "environment" {
  description = "The Deployment environment"
}

variable "aws_region" {
  description = "The region to launch the bastion host"
}

variable "subnets_id" {
  type = any
}

variable "vpc_id" {
  description = "VPC ID"
}

variable "sg_id" {
  description = "Security Group ID"
}

variable "log_stream_prefix" {
  description = "Prefix for CloudWatch Logs stream name"
  default     = "interviewapi"  # Replace with your desired prefix
}