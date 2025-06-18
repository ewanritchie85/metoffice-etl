resource "aws_ecs_cluster" "ecs_cluster" {
  name = var.ecs_cluster_name
}

output "ecs_cluster_arn" {
  value = aws_ecs_cluster.ecs_cluster.arn
}

output "ecs_execution_role_arn" {
  value = aws_iam_role.ecs_exec_role.arn
}

resource "aws_ecs_task_definition" "etl_task" {
  family                   = "metoffice-etl-task"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  network_mode             = "awsvpc"
  execution_role_arn       = aws_iam_role.ecs_exec_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn


  container_definitions = jsonencode([
    {
      name      = "${var.container_name}"
      image     = "${var.ecr_image_path}"
      essential = true


      environment = [
        {
          name  = "TRIGGERED_BY"
          value = "eventbridge"
        },
        {
          name  = "METOFFICE_API_KEY"
          value = "${var.metoffice_api_key}"
        },
        {
          name  = "LANDING_BUCKET_NAME"
          value = "${var.landing_bucket_name}"
        },
        {
          name  = "DB_HOST"
          value = "${var.db_host}"
        },
        {
          name  = "DB_HOST"
          value = aws_db_instance.etl_db.address
        },
        {
          name  = "DB_PORT"
          value = tostring(aws_db_instance.etl_db.port)
        },
        {
          name  = "DB_NAME"
          value = aws_db_instance.etl_db.db_name
        },
        {
          name  = "DB_USER"
          value = aws_db_instance.etl_db.username
        },
        {
          name  = "DB_PASSWORD"
          value = "${var.loading_db_password}"
        },
        {
          name  = "RUNNING_IN_ECS"
          value = "true"
        }
      ]



      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/metoffice-etl"
          awslogs-region        = "${var.aws_region}"
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/metoffice-etl"
  retention_in_days = 7

}
