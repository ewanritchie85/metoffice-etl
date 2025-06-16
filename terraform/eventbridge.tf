resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name                = "daily-metoffice-trigger"
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "ecs_target" {
  rule      = aws_cloudwatch_event_rule.daily_trigger.name
  target_id = "metofficeETLTask"
  arn       = aws_ecs_cluster.ecs_cluster.arn
  role_arn  = aws_iam_role.ecs_events_role.arn

  ecs_target {
    launch_type         = "FARGATE"
    platform_version    = "LATEST"
    task_definition_arn = aws_ecs_task_definition.etl_task.arn
    network_configuration {
      subnets          = [aws_subnet.private_a.id, aws_subnet.private_b.id]
      assign_public_ip = true
      security_groups  = [aws_security_group.ecs_service_sg.id]
    }
  }
}