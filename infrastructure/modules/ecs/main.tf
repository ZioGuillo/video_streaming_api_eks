terraform {

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.29.0"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = var.aws_region

  default_tags {
    tags = {
      ManagedByTerraform = true
      Environment        = var.environment
      TerraformLocation  = ""
    }
  }
}