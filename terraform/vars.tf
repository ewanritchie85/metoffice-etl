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

}

variable "loading_db_name" {
  description = "Name of RDS for loading clean data"
  type        = string

}

variable "loading_db_username" {
  # stored in terraform cloud
  description = "Username for loading db access"
  type        = string
}

variable "loading_db_password" {
  # stored in terraform cloud
  description = "DB password"
  type        = string
}

variable "vpc_id" {
  description = "DB VPC id"
  type        = string
}

variable "my_ip_cidr" {
  description = "Local IP CIDR"
  type        = string
}

variable "ecr_image_path" {
  description = "path to image file in ECR "
  type        = string
}

variable "ecs_cluster_name" {
  description = "name of aws ecs cluster"
  type        = string

}



variable "container_name" {
  description = "name of ETL container image"
  type        = string

}

variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "subnet_private_a_name" {
  description = "Name of the first private subnet"
  type        = string
}

variable "subnet_private_b_name" {
  description = "Name of the second private subnet"
  type        = string
}
