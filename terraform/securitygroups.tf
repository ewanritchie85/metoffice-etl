# ECS Security Group
resource "aws_security_group" "ecs_service_sg" {
  name        = "ecs-service-sg"
  description = "Security group for ECS tasks"
  vpc_id      = aws_vpc.main.id

}

# RDS Security Group
resource "aws_security_group" "db_sg" {
  name        = "db-sg"
  description = "Security group for RDS instance"
  vpc_id      = aws_vpc.main.id
}

resource "aws_security_group_rule" "rds_from_ecs" {
  type                     = "ingress"
  from_port                = 3306
  to_port                  = 3306
  protocol                 = "tcp"
  security_group_id        = aws_security_group.db_sg.id
  source_security_group_id = aws_security_group.ecs_service_sg.id
  description              = "Allow MySQL from ECS"
}


resource "aws_security_group_rule" "rds_local_access" {
  type              = "ingress"
  from_port         = 3306
  to_port           = 3306
  protocol          = "tcp"
  cidr_blocks       = [var.my_ip_cidr] 
  security_group_id = aws_security_group.db_sg.id
  description       = "Temporary local access fo dbeaver"
}

resource "aws_security_group_rule" "rds_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.db_sg.id
  description       = "Allow all outbound traffic"
}

# Add strict egress for MySQL from ECS to RDS
resource "aws_security_group_rule" "ecs_https_egress" {
  type              = "egress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.ecs_service_sg.id
  description       = "Allow HTTPS outbound for Met Office API"
}
resource "aws_security_group_rule" "ecs_mysql_egress" {
  type                     = "egress"
  from_port                = 3306
  to_port                  = 3306
  protocol                 = "tcp"
  security_group_id        = aws_security_group.ecs_service_sg.id
  source_security_group_id = aws_security_group.db_sg.id
  description              = "Allow MySQL egress to RDS"
}
