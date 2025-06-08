resource "aws_s3_bucket" "landing_bucket" {
  bucket = var.landing_bucket_name
  force_destroy = true


 
}