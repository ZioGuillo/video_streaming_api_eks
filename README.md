# Video Streaming API on AWS EKS

[![Push Docker Image w Tag](https://github.com/ZioGuillo/video_streaming_api_eks/actions/workflows/docker_push_and_version.yaml/badge.svg?branch=master)](https://github.com/ZioGuillo/video_streaming_api_eks/actions/workflows/docker_push_and_version.yaml) ![OWASP Check](https://github.com/ZioGuillo/video_streaming_api_eks/actions/workflows/OWASP_scan.yaml/badge.svg)

## Project Description

This repository contains infrastructure code for deploying a scalable, highly-available video streaming API using Amazon EKS (Elastic Kubernetes Service). It uses Terraform and Terragrunt for a modular and efficient infrastructure setup across multiple AWS environments.

## Application Specifications

- **Streaming API**: Designed to handle high-volume video streaming.
- **Scalability**: Dynamically scales to accommodate fluctuating user loads.
- **Resiliency**: Distributed across multiple Availability Zones for high availability.
- **Security**: Configured with best practices to secure video content and user data.

## Features

- **Amazon EKS Cluster**: Fully managed Kubernetes service.
- **Auto-Scaling**: Worker nodes configured to auto-scale.
- **Multi-AZ VPC**: Spanning multiple Availability Zones for fault tolerance.
- **Security**: Enhanced with security groups and network configurations.

## Prerequisites

- AWS Account and CLI setup.
- Terraform and Terragrunt installed.

## Installation & Deployment

1. Clone the repository.
2. Navigate to the desired environment under `environments/`.
3. Run `terragrunt init` to initialize the environment.
4. Apply the configuration using `terragrunt apply`.
5. `aws eks update-kubeconfig --name name-0f-the-cluster --region us-east-1`

## Modules

- **VPC**: Configures a VPC across multiple AZs.
- **EKS Cluster**: Sets up the EKS cluster.
- **Worker Nodes**: Manages the auto-scaling group for worker nodes.

## Environments

- Development
- Staging
- Production

Each environment is isolated and can be configured separately.

## Contributing

We welcome contributions. Please adhere to the project's contribution guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- AWS EKS Documentation
- Terraform and Terragrunt Communities
