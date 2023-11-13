# VPC

Creating 1 VPC, multiple subnets(Public and Private), 1 Internet gateway, 1 security group, In addition, we will create Custom Route Tables and associate them with subnets with NAT gateway support.

## Overview

Amazon Resources Created Using Terraform
AWS VPC with 10.0.0.0/16 CIDR.
Multiple AWS VPC public subnets would be reachable from the internet; which means traffic from the internet can hit a machine in the public subnet.
Multiple AWS VPC private subnets which mean it is not reachable to the internet directly without NAT Gateway.
AWS VPC Internet Gateway and attach it to AWS VPC.
Public and private AWS VPC Route Tables.
AWS VPC NAT Gateway.
Associating AWS VPC Subnets with VPC route tables.


