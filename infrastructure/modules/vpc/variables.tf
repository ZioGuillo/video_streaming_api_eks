variable "name" {
  description = "Name of the project"
}

variable "environment" {
  description = "The Deployment environment"
}

variable "vpc_cidr" {
  description = "First 2 numbers of a dotted-quad IP address. Example: \"10.205\"."
  type        = string
  validation {
    condition     = length(regexall("^\\d{1,3}\\.\\d{1,3}$", var.vpc_cidr)) > 0
    error_message = "The 'cidr_base' value must be 2 numbers separated by a dot."
  }
}

variable "public_subnets_cidr" {
  type        = list
  description = "The CIDR block for the public subnet"
}

variable "private_subnets_cidr" {
  type        = list
  description = "The CIDR block for the private subnet"
}

variable "aws_region" {
  description = "The region to launch the bastion host"
}

variable "availability_zones" {
  type        = list(string)
  description = "List of Availability Zones (e.g., ['us-east-1a', 'us-east-1b', 'us-east-1c'])"
  default     = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

variable "num_availability_zones" {
  type        = number
  description = "Number of Availability Zones to use"
  default     = 1
}

variable "default-tags" {
  type        = map(string)
  description = "Map of default tags for AWS resources"

  default = {
    ManagedByTerraform = "True"
  }
}