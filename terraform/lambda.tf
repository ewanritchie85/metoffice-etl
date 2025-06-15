resource "aws_lambda_function" "metoffice_etl" {
  function_name = "metoffice-etl"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "extract.extract.lambda_handler"
  runtime       = "python3.12"

  s3_bucket = var.landing_bucket_name
  s3_key    = var.lambda_package_key


  environment {
    variables = {
      LANDING_BUCKET = var.landing_bucket_name
    }
  }
}