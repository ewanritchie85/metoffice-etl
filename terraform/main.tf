terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
    required_version = ">= 1.0"
}
terraform {
  backend "remote" {
    organization = "ewanritchie85-org"

    workspaces {
      name = "metoffice-etl"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  default_tags {
    tags = {
      Environment = "Dev"
      Project     = "MetOffice-ETL"
    }
  }

}