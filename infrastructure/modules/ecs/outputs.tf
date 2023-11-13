# The name of the ECS cluster
output "ecs_cluster_name" {
  value = aws_ecs_cluster.ecs_cluster.name
}

# The ARN of the ECS task definition
#output "ecs_task_definition_arn" {
  #value = aws_ecs_task_definition.task_definition.arn
#}

# The name of the IAM role for ECS task execution
#output "ecs_execution_role_name" {
  #value = aws_iam_role.ecs_execution_role.name
#}

output "public_ip" {
  value = data.aws_network_interface.api-cluster.association[0].public_ip
}