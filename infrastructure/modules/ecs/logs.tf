resource "aws_cloudwatch_log_group" "api_log_group" {
  name = "api-log-group"  # Replace with your desired log group name
}

resource "aws_cloudwatch_log_stream" "api_log_stream" {
  name           = "api-log-stream-${var.log_stream_prefix}"  # Replace with your desired log stream name
  log_group_name = aws_cloudwatch_log_group.api_log_group.name  # Reference to the log group created earlier
}
