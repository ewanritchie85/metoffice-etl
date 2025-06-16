resource "aws_iam_role" "ecs_exec_role" {
  name = "ecs-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_logs" {
  role       = aws_iam_role.ecs_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_policy" "ecs_s3_policy" {
  name = "ecs-s3-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = [
        "s3:PutObject",
        "s3:GetObject"
      ],
      Effect   = "Allow",
      Resource = "arn:aws:s3:::${var.landing_bucket_name}/*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_s3_attach" {
  role       = aws_iam_role.ecs_exec_role.name
  policy_arn = aws_iam_policy.ecs_s3_policy.arn
}

resource "aws_iam_role" "ecs_events_role" {
  name = "ecs-events-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "events.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "ecs_run_task_policy" {
  name = "ecs-run-task-policy"
  role = aws_iam_role.ecs_events_role.id

  # waits until the following are created 
  depends_on = [
    aws_ecs_task_definition.etl_task,
    aws_iam_role.ecs_exec_role
  ]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "ecs:RunTask"
      ]
      Resource = aws_ecs_task_definition.etl_task.arn
    }, {
      Effect = "Allow"
      Action = [
        "iam:PassRole"
      ]
      Resource = aws_iam_role.ecs_exec_role.arn
    }]
  })
}