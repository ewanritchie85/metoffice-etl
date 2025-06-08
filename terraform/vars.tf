variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string

}

variable "aws_profile" {
  description = "AWS profile to use for authentication"
  type        = string
  
}

variable "landing_bucket_name" {
  description = "Name of the S3 bucket for landing data"
  type        = string
  default     = "metoffice-landing-bucket"
  
}