# Security group for the ECS tasks
resource "aws_security_group" "ecs_sg" {
  vpc_id = var.vpc_id  # VPC ID
  name   = "ecs-security-group"
  # Inbound and outbound rules
  ingress {
    from_port   = 3246
    to_port     = 3246
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}