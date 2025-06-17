resource "aws_db_instance" "loading_db" {
  db_name              = var.loading_db_name
  instance_class       = "db.t3.micro"
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "8.0"
  username             = var.loading_db_username
  password             = var.loading_db_password
  publicly_accessible  = false
  db_subnet_group_name = aws_db_subnet_group.main.name

  vpc_security_group_ids    = [aws_security_group.db_sg.id]
  skip_final_snapshot       = true
  final_snapshot_identifier = "do-not-create"
  depends_on = [
    aws_db_subnet_group.main,
    aws_security_group.db_sg,
    aws_subnet.private_a,
    aws_subnet.private_b
  ]
}

resource "aws_security_group" "db_sg" {
  name        = "allow-mysql-from-my-ip"
  description = "Allows access to RDS from local IP"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow MySQL from ECS"
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_service_sg.id]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_db_subnet_group" "main" {
  name       = "metoffice-db-subnet-group"
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]

  tags = {
    Name = "metoffice-db-subnet-group"
  }
}
