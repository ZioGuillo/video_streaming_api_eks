locals {
  # Automatically load region-level variables
  region_vars = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  # Automatically load environment-level variables
  environment_vars = read_terragrunt_config(find_in_parent_folders("environment.hcl"))

  # Extract the variables we need for easy access
  aws_region   = local.region_vars.locals.aws_region
  environment  = local.environment_vars.locals.environment
  
}

terraform {
  source = "${get_terragrunt_dir()}../../../../../../modules//ecs"
}

include {
  path = find_in_parent_folders()
}
dependency "vpc" {
  config_path = "../vpc"
}

inputs = {

  subnets_id = dependency.vpc.outputs.private_subnets_id
  vpc_id     = dependency.vpc.outputs.vpc_id
  sg_id      = dependency.vpc.outputs.default_sg_id

}
