# 🚀 Production DevOps Project — AWS, Docker, Kubernetes, Jenkins, Terraform

> A hands-on, end-to-end DevOps project built from scratch — covering networking, containers, CI/CD, infrastructure as code, and monitoring on AWS.

---

## 📋 Project Overview

This project simulates a real-world production DevOps environment. Starting from zero, the goal is to build a fully automated pipeline that takes code from a developer's laptop to a live, monitored application running on Kubernetes — with every piece of infrastructure defined as code.

**Target Stack:**
`AWS` · `Linux` · `Docker` · `Kubernetes (EKS)` · `Jenkins` · `Terraform` · `Prometheus` · `Grafana` · `CloudWatch`

---

## 🗺️ Project Roadmap

| Phase | Topic | Status |
|-------|-------|--------|
| Phase 1 | AWS Networking + Linux + EC2 Setup | ✅ Complete |
| Phase 2 | Git + GitHub + Docker + ECR | ✅ Complete |
| Phase 3 | Terraform — Infrastructure as Code | 🔄 In Progress |
| Phase 4 | Kubernetes on EKS | 🔜 Upcoming |
| Phase 5 | Jenkins CI/CD Pipeline | 🔜 Upcoming |
| Phase 6 | Monitoring — Prometheus, Grafana, CloudWatch | 🔜 Upcoming |

---

## ✅ Phase 1 — AWS Networking & Linux Foundation

### Goal
Build a secure, production-grade network on AWS from scratch — with a public-facing Jenkins server and a fully isolated private app server communicating only via private IP.

### Architecture

```
Internet
    ↓
Internet Gateway
    ↓
Route Table (0.0.0.0/0 → IGW)
    ↓
┌─────────────────────────────────────────┐
│           VPC — 10.0.0.0/16             │
│                                         │
│  ┌──────────────┐   ┌────────────────┐  │
│  │ Public Subnet│   │ Private Subnet │  │
│  │ 10.0.1.0/24  │   │ 10.0.2.0/24   │  │
│  │              │   │                │  │
│  │ Jenkins EC2  │──▶│  App EC2       │  │
│  │ (public IP)  │   │ (no public IP) │  │
│  └──────────────┘   └────────────────┘  │
│         ↓                               │
│    NAT Gateway                          │
│  (outbound only for private subnet)     │
└─────────────────────────────────────────┘
```

### AWS Components Built

| Component | Configuration |
|-----------|--------------|
| VPC | 10.0.0.0/16 |
| Public Subnet | 10.0.1.0/24 — us-east-1a |
| Private Subnet | 10.0.2.0/24 — us-east-1a |
| Internet Gateway | Attached to VPC |
| NAT Gateway | In public subnet with Elastic IP |
| Public Route Table | 0.0.0.0/0 → IGW |
| Private Route Table | 0.0.0.0/0 → NAT Gateway |
| Jenkins Security Group | Port 22 (your IP), 8080 (your IP), 80/443 (open) |
| App Security Group | Port 22 from Jenkins SG only |

### EC2 Instances

| Instance | Subnet | Type | Purpose |
|----------|--------|------|---------|
| devops-jenkins-server | Public | t2.medium | Jenkins, Docker, all tools |
| devops-app-server | Private | t2.micro | Application server |

### Tools Installed on Jenkins Server

```bash
Java 17        # Jenkins dependency
Jenkins        # CI/CD server
Docker         # Container runtime
Git            # Version control
AWS CLI        # AWS access from terminal
kubectl        # Kubernetes CLI
Terraform      # Infrastructure as Code
```

### Linux Networking Commands Practiced

```bash
ip addr show           # View network interfaces and IPs
ip route show          # View routing table
ping -c 4 google.com   # Test connectivity
ss -tulpn              # View listening ports and services
curl http://localhost:5000  # Test service response
traceroute google.com  # Trace network path
nslookup google.com    # DNS resolution check
ifconfig               # View interface configuration
```

### Mistakes Made & Fixed

**❌ Mistake 1 — DB not connecting to web server**
Both EC2 instances were in different VPCs. Two VPCs = two isolated networks with no communication path.
**Fix:** Placed both instances in the same VPC. Private IP communication worked immediately.

**❌ Mistake 2 — Wrong VPC selected during instance launch**
AWS has a default VPC that is easy to accidentally select during quick EC2 setup.
**Fix:** Always explicitly select the correct VPC during instance configuration. Double check before launching.

**❌ Mistake 3 — Security group misconfigured**
The app server security group was not allowing inbound traffic from the Jenkins server.
**Fix:** Updated inbound rules to use the Jenkins security group ID as the source — not 0.0.0.0/0. Least privilege always.

---

## ✅ Phase 2 — Git, GitHub & Docker

### Goal
Containerize the application, version control the code on GitHub, and push the Docker image to AWS ECR — ready for Kubernetes deployment.

### What Was Built

```
Flask App (Python)
    ↓
Git init + commit
    ↓
GitHub Repository (SSH auth)
    ↓
Dockerfile written
    ↓
Docker image built
    ↓
Container tested locally
    ↓
Image pushed to AWS ECR
```

### Application — Python Flask

The app exposes three endpoints used throughout the project:

| Endpoint | Purpose |
|----------|---------|
| `/` | Main response — returns app info as JSON |
| `/health` | Health check — used by Kubernetes and ALB |
| `/metrics` | Prometheus metrics scraping endpoint |

```
devops-project/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container definition
└── .gitignore          # Ignored files
```

### Dockerfile Explained

```dockerfile
FROM python:3.11-slim       # Lightweight base image
WORKDIR /app                # Set working directory inside container
COPY requirements.txt .     # Copy deps first (Docker layer cache)
RUN pip install --no-cache-dir -r requirements.txt  # Install deps
COPY . .                    # Copy application code
EXPOSE 5000                 # Document the port
CMD ["python3", "app.py"]   # Start the app
```

> **Pro tip:** Always `COPY requirements.txt` and run `pip install` before `COPY . .` — this caches the dependency layer so rebuilds are significantly faster when only app code changes.

### Git Workflow Used

```bash
git init                          # Initialise local repo
git config --global user.name ""  # Set identity
git config --global user.email "" # Set identity
git add .                         # Stage all files
git commit -m "message"           # Commit snapshot
git remote add origin <ssh-url>   # Link to GitHub
git push -u origin main           # Push to remote
```

### GitHub SSH Setup

SSH key authentication was configured so the EC2 server can push to GitHub without password prompts — the production-grade approach used in CI/CD pipelines.

```bash
ssh-keygen -t ed25519 -C "email"   # Generate key pair
cat ~/.ssh/id_ed25519.pub           # Copy public key to GitHub
ssh -T git@github.com               # Verify connection
```

### Docker Commands Used

```bash
docker build -t devops-project:v1 .          # Build image
docker run -d -p 5000:5000 devops-project:v1 # Run container
docker ps                                     # List running containers
docker logs devops-app                        # View container logs
docker images                                 # List local images
```

### AWS ECR — Push Image

```bash
# Create ECR repository
aws ecr create-repository --repository-name devops-project --region us-east-1

# Authenticate Docker with ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag devops-project:v1 <account-id>.dkr.ecr.us-east-1.amazonaws.com/devops-project:v1
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/devops-project:v1
```

### Mistakes Made & Fixed

**❌ Mistake 1 — Pushed sensitive files to GitHub**
Accidentally included test config files with credentials before `.gitignore` was set up.
**Fix:** Always create `.gitignore` before the first `git add`. Add `.env`, `*.pem`, and credential files immediately.

**❌ Mistake 2 — Docker permission errors**
`docker: permission denied` when running commands as the ubuntu user.
**Fix:** Added ubuntu user to the docker group with `sudo usermod -aG docker ubuntu` then started a fresh SSH session.

**❌ Mistake 3 — ECR push rejected**
Docker push failed because ECR requires authentication before accepting images.
**Fix:** Always run `aws ecr get-login-password` and pipe it to `docker login` before any push command.

---

## 🔜 Phase 3 Preview — Terraform

Everything built in Phase 1 manually (clicking in the AWS console) will be destroyed and rebuilt 100% as Terraform code.

Files that will be created:
```
terraform/
├── main.tf           # Core resources
├── vpc.tf            # VPC, subnets, IGW, NAT, route tables
├── ec2.tf            # EC2 instances and key pairs
├── security.tf       # Security groups
├── ecr.tf            # ECR repository
├── variables.tf      # Input variables
├── outputs.tf        # Output values
└── backend.tf        # Remote state — S3 + DynamoDB
```

---

## 🛠️ Prerequisites

To follow along with this project you will need:

- An AWS account with IAM user and programmatic access
- AWS CLI configured locally (`aws configure`)
- A GitHub account
- Basic Linux command line knowledge
- An SSH client

---

## 📚 Key Concepts Covered So Far

| Concept | Where Used |
|---------|-----------|
| VPC & subnets | Phase 1 — network isolation |
| Internet Gateway | Phase 1 — public internet access |
| NAT Gateway | Phase 1 — private subnet outbound |
| Security Groups | Phase 1 — instance-level firewall |
| Bastion / Jump Server | Phase 1 — secure SSH access pattern |
| Git version control | Phase 2 — code management |
| SSH key auth | Phase 2 — GitHub authentication |
| Docker & containers | Phase 2 — application packaging |
| AWS ECR | Phase 2 — container image registry |

---

## 👤 Author

Built as a hands-on learning project to develop real-world DevOps engineering skills.

Connect on LinkedIn → https://www.linkedin.com/in/mahesh-gadhave-xamarin-maui-developer/

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
