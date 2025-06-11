resource "aws_db_instance" "loading_db" {
  db_name                = var.loading_db_name
  instance_class         = "db.t3.micro"
  allocated_storage      = 10
  engine                 = "mysql"
  engine_version         = "8.0"
  username               = var.loading_db_username
  password               = var.loading_db_password
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.db_sg.id]

}

resource "aws_security_group" "db_sg" {
  name        = "allow-mysql-from-my-ip"
  description = "Allows access to RDS from local IP"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow MySQL"
    from_port = 3306
    to_port = 3306
    protocol = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
