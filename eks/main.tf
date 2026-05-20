provider "aws" {
  region = var.region
}

data "terraform_remote_state" "vpc" {
  backend = "local"

  config = {
    path = var.vpc_state_path
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.37.1"

  cluster_name    = var.cluster_name
  cluster_version = "1.30"

  cluster_endpoint_public_access = true

  create_kms_key            = false
  cluster_encryption_config = {}

  vpc_id     = data.terraform_remote_state.vpc.outputs.vpc_id
  subnet_ids = data.terraform_remote_state.vpc.outputs.public_subnets

  enable_cluster_creator_admin_permissions = true

  eks_managed_node_groups = {
    cpu = {
      name           = "cpu-node-group"
      instance_types = ["t3.micro"]

      min_size     = 1
      max_size     = 5
      desired_size = 4

      labels = {
        workload = "cpu"
      }
    }

    gpu = {
      name           = "gpu-node-group"
      instance_types = ["t3.micro"]

      min_size     = 1
      max_size     = 4
      desired_size = 3

      labels = {
        workload = "gpu"
      }
    }
  }

  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}