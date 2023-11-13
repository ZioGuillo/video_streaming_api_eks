resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet[0].id
  # Other NAT Gateway configuration
  tags = {
    Name        = "nat"
    Environment = "${var.environment}"
  }
}
