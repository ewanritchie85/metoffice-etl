


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

  container_definitions = jsonencode([
    {
      name      = "${var.container_name}"
      image     = "${var.ecr_image_path}"
      essential = true
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

