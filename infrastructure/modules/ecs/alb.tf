/* Application Load Balancer (ALB)
resource "aws_lb" "my_alb" {
  name               = "my-alb"
  internal           = false
  load_balancer_type = "application"
  enable_deletion_protection = false
  subnets            = aws_subnet.public_subnet[*].id
  enable_http2       = true

  tags = {
    Name = "my-alb"
  }
}*/

/* Target Group for ALB 
resource "aws_lb_target_group" "my_target_group" {
  name     = "my-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.vpc.id
}

/* Listener Rule for ALB 
resource "aws_lb_listener_rule" "my_listener_rule" {
  listener_arn = aws_lb.my_alb.arn
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.my_target_group.arn
  }
  condition {
    path_pattern {
      values = ["/test/"]
    }
  }
}*/