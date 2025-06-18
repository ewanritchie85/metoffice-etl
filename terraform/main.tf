terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "remote" {
    organization = "ewanritchie85-org"

    workspaces {
      name = "metoffice-etl"
    }
  }
    required_version = ">= 1.0"
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