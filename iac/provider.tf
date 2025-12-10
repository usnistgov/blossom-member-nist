terraform {
  backend "s3" {
    # variables cannot be used here
    bucket = "nist-blossom-iac"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.12.0" # "5.27.0" the last pre-update version without Python 3.13
    }
  }
}

provider "aws" {
  region = var.aws_region
}
