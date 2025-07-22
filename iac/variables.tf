module "vars" {
  source = "./module/vars"
  # Use the selected terraform workspace to select the environment by json-file name
  environment       = terraform.workspace
  configuration_dir = "./configurations"
}

locals {
  # Older-style compositional naming of lambda
  # prefix = "b-${module.vars.env.network_name}-${lower(module.vars.env.member_name)}" core_bucket_name
  prefix = "b-${lower(module.vars.env.core_bucket_name)}"

  s3_lambda_suffix  = "${lower(module.vars.env.lambda_s3_suffix)}"
  s3_watched_uri    = "${module.vars.env.s3_watched_uri}"
  ec2_lambda_suffix = "${lower(module.vars.env.lambda_ec2_suffix)}"
  ec2_instance_id   = "${module.vars.env.ec2_instance_id}"
  # These variables will become tags on the deployed entities
  tags = {
    "Terraform"             = "true"
    "Blossom_Network_Name"  = module.vars.env.network_name
    "Blossom_Member_Name"   = module.vars.env.member_name
    "Updated_On"            = formatdate("YYYY-MM-DD hh:mm:ss ZZZ", timestamp())
    "Updated_By"            = "Terraform"

    ### These are nice to have tags for every ORG deployment,
    ### but these particular values are NIST-specific
    "Group"                 = "772.03"
    "Members"               = "SAM-NIST and NIST"
    "Network_Version"       = "Blossom v3"
    "Owner_Contact"         = "blossom@nist.gov"
  }
}

variable "hlf_debug" {
  type        = bool
  default     = false
  sensitive   = false
  description = "Enables HFC debug logging on the query lambda"
}

variable "cognito_debug" {
  type        = bool
  default     = true
  sensitive   = false
  description = "Enables localhost callback URLs in the Cognito user pool client"
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  sensitive   = false
  description = "The AWS region to use"
}