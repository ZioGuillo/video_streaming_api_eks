# ECS task definition
resource "aws_ecs_task_definition" "task_definition" {
  family                = "api-task"
  network_mode          = "awsvpc"
  memory                = "512"
  requires_compatibilities = ["FARGATE"]

  # Task execution role (Replace "XXX" with your IAM role ARN)
  execution_role_arn    = aws_iam_role.ecs_execution_role.arn  

  # Container definition with log configuration
  container_definitions = jsonencode([
    {
      name      = "api-container"
      image     = "cdfuller/echo-server:latest"
      # https://github.com/cdfuller/echo-server
      # image     = "mendhak/http-https-echo:30"
      # https://github.com/mendhak/docker-http-https-echo
      cpu       = 256
      memory    = 512
      port_mappings = [
        {
          container_port = 3246
          host_port      = 3246
          protocol       = "tcp"
        }
      ],
      log_configuration = {
        log_driver = "awslogs"
        options = {
          "awslogs-create-group" = true
          "awslogs-group"   = aws_cloudwatch_log_group.api_log_group.name  # Use the log group name you created
          "awslogs-region"  = var.aws_region 
          "awslogs-stream-prefix" = var.log_stream_prefix
        }
      }
    }
  ])

  # Defining the task-level CPU
  cpu = "256"  
}

# ECS service
resource "aws_ecs_cluster" "ecs_cluster" {
  name = "api-cluster"  
}

resource "aws_ecs_service" "service" {
  name            = "api-service"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.task_definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  # Network configuration
  network_configuration {
    subnets            = var.subnets_id
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}
