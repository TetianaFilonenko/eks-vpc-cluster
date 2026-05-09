# EKS + VPC Infrastructure with Terraform

## Description

This project creates AWS infrastructure using Terraform:

- VPC (network)
- EKS (Kubernetes cluster)
- 2 node groups:
  - CPU
  - GPU

Official Terraform modules used:
- terraform-aws-modules/vpc/aws
- terraform-aws-modules/eks/aws

---

## Project Structure

eks-vpc-cluster/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tf
├── backend.tf
├── README.md
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tf
│   └── backend.tf
├── eks/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tf
│   └── backend.tf

---

## Requirements

- Terraform >= 1.0
- AWS CLI
- kubectl
- Configured AWS profile (AWS_PROFILE)

---

## Usage

### 1. Initialize Terraform

terraform init

### 2. Validate configuration

terraform validate

### 3. Create infrastructure

terraform apply

---

## Connect to EKS

aws eks --region eu-central-1 update-kubeconfig --name lab-eks-cluster

kubectl get nodes

---

## Result

After running Terraform:

- VPC is created
- EKS cluster is created
- 2 node groups (CPU and GPU) are running
- Nodes are accessible via kubectl

---

## Destroy infrastructure

terraform destroy

Important: Always destroy resources after use to avoid unnecessary AWS costs.

---

## Author

Tetiana Filonenko