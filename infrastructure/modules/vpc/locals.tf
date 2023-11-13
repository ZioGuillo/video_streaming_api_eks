locals {
  default-tags = {
    ManagedByTerraform = true
  }
  #production_availability_zones = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
}