variable "region" {
  default = "eu-central-1"
}

variable "cluster_name" {
  default = "lab-eks-cluster"
}

variable "vpc_state_path" {
  default = "../vpc/terraform.tfstate"
}