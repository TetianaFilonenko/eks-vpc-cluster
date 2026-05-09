# EKS + VPC + ArgoCD Infrastructure with Terraform

## Description

This project creates AWS infrastructure using Terraform:

- VPC (network)
- EKS (Kubernetes cluster)
- 2 node groups:
  - CPU
  - GPU
- ArgoCD (GitOps continuous delivery)

Official Terraform modules and providers used:

- terraform-aws-modules/vpc/aws
- terraform-aws-modules/eks/aws
- Helm provider (ArgoCD chart v5.51.6)
- Kubernetes provider

---

## Project Structure

```
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
└── terraform/
    └── argocd/
        ├── main.tf
        ├── variables.tf
        ├── outputs.tf
        ├── terraform.tf
        ├── backend.tf
        └── values/
            └── argocd-values.yaml
```

---

## Requirements

- Terraform >= 1.0
- AWS CLI
- kubectl
- Configured AWS profile (AWS_PROFILE)

---

## Usage

Each module is applied separately in order:

### 1. VPC

```bash
cd vpc
terraform init
terraform apply
```

### 2. EKS

```bash
cd eks
terraform init
terraform apply
```

### 3. Connect to EKS

```bash
aws eks --region eu-central-1 update-kubeconfig --name lab-eks-cluster
kubectl get nodes
```

### 4. ArgoCD

```bash
cd terraform/argocd
terraform init
terraform apply
```

---

## ArgoCD Access

Run port-forward:

```bash
kubectl port-forward svc/argocd-server -n infra-tools 8080:443
```

Open in browser:

```
http://localhost:8080
```

Login — username: `admin`, password:

```bash
kubectl get secret argocd-initial-admin-secret -n infra-tools -o jsonpath="{.data.password}" | base64 --decode && echo
```

---

## Result

After running Terraform:

- VPC is created
- EKS cluster is created
- 2 node groups (CPU and GPU) are running
- Nodes are accessible via kubectl
- ArgoCD is deployed in the `infra-tools` namespace

---

## Destroy infrastructure

Destroy in reverse order:

```bash
cd terraform/argocd && terraform destroy
cd eks && terraform destroy
cd vpc && terraform destroy
```

> **Important:** Always destroy resources after use to avoid unnecessary AWS costs.
