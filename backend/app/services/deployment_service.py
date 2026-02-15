from pathlib import Path
from typing import Dict

class DeploymentService:
    
    def generate_github_actions(self, spec: Dict) -> str:
        """Generate GitHub Actions CI/CD pipeline"""
        return f"""name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest
      - name: Security scan
        run: |
          pip install bandit
          bandit -r backend/
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: echo "Deploying..."
"""
    
    def generate_kubernetes_manifests(self, spec: Dict) -> Dict[str, str]:
        """Generate Kubernetes deployment manifests"""
        app_name = spec.get("appConfig", {}).get("name", "app").lower().replace(" ", "-")
        
        deployment = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: backend
        image: {app_name}:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: {app_name}-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: {app_name}-service
spec:
  selector:
    app: {app_name}
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
"""
        
        ingress = f"""apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {app_name}-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - {app_name}.example.com
    secretName: {app_name}-tls
  rules:
  - host: {app_name}.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {app_name}-service
            port:
              number: 80
"""
        
        return {
            "deployment.yaml": deployment,
            "ingress.yaml": ingress
        }
    
    def generate_terraform_aws(self, spec: Dict) -> str:
        """Generate Terraform for AWS deployment"""
        app_name = spec.get("appConfig", {}).get("name", "app").lower().replace(" ", "-")
        
        return f"""terraform {{
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

provider "aws" {{
  region = "us-east-1"
}}

resource "aws_ecs_cluster" "{app_name}_cluster" {{
  name = "{app_name}-cluster"
}}

resource "aws_ecs_task_definition" "{app_name}_task" {{
  family                   = "{app_name}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  
  container_definitions = jsonencode([{{
    name  = "{app_name}"
    image = "{app_name}:latest"
    portMappings = [{{
      containerPort = 8000
      protocol      = "tcp"
    }}]
  }}])
}}

resource "aws_lb" "{app_name}_lb" {{
  name               = "{app_name}-lb"
  internal           = false
  load_balancer_type = "application"
  subnets            = ["subnet-xxx", "subnet-yyy"]
}}

output "load_balancer_dns" {{
  value = aws_lb.{app_name}_lb.dns_name
}}
"""
    
    def generate_monitoring(self, spec: Dict) -> Dict[str, str]:
        """Generate Prometheus and Grafana configs"""
        prometheus = """global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['localhost:8000']
"""
        
        grafana_dashboard = """{
  "dashboard": {
    "title": "Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [{"expr": "rate(http_requests_total[5m])"}]
      },
      {
        "title": "Error Rate",
        "targets": [{"expr": "rate(http_requests_total{status=~\"5..\"}[5m])"}]
      },
      {
        "title": "Response Time",
        "targets": [{"expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket)"}]
      }
    ]
  }
}"""
        
        return {
            "prometheus.yml": prometheus,
            "grafana-dashboard.json": grafana_dashboard
        }
