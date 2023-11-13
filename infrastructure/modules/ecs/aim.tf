# Define an IAM role for ECS task execution
resource "aws_iam_role" "ecs_execution_role" {
  name = "ecs_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "ecs_execution_policy" {
  name        = "ecs_execution_policy"
  description = "IAM policy for ECS task execution role"
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "logs:CreateLogGroup",
        Effect = "Allow",
        Resource = "*"
      },
      {
        Action = "ecs:ListTasks",
        Effect = "Allow",
        Resource = "*"
      },
      {
        Action = "ecs:DescribeTasks",
        Effect = "Allow",
        Resource = "*"
      },
  
    ]
  })
}

# Attach the CloudWatchLogsFullAccess policy to the ECS task execution role
resource "aws_iam_policy_attachment" "ecs_execution_role_cloudwatch" {
  name = "ecs_execution_role_cloudwatch"
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
  roles      = [aws_iam_role.ecs_execution_role.name]
}


# Attach an IAM policy to the ECS task execution role (if needed)
# resource "aws_iam_policy_attachment" "example" {
#   policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
#   roles      = [aws_iam_role.ecs_execution_role.name]
# }