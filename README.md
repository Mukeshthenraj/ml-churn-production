
# 🚀 ML Churn Prediction Production System (End‑to‑End MLOps Platform)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-blue)
![AWS](https://img.shields.io/badge/AWS-EC2-orange)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-yellow)
![CI/CD](https://img.shields.io/badge/GitHub-Actions-blue)

---

![Dashboard](docs/screenshots/dashboard-overview.png)

This repository demonstrates a **complete production-style Machine Learning system** for predicting **customer churn**.

The project covers the **entire lifecycle of an ML system**, including:

• Model training  
• API development  
• Containerization  
• Monitoring & observability  
• Kubernetes orchestration  
• Cloud deployment on AWS  
• CI/CD automation  

The goal is to show **how a real ML service is built, deployed, monitored, and maintained in production**.

---

# 🧠 Machine Learning Model

The churn model is trained using **Scikit‑learn** and typical preprocessing techniques used in production ML pipelines.

### Training Pipeline

Implemented in:

src/ml/train.py

Steps:

1. Load customer churn dataset
2. Preprocess categorical and numerical features
3. Apply **OneHotEncoding** for categorical variables
4. Train model using **Scikit‑learn**
5. Serialize trained model using **joblib**
6. Store model artifact for API inference

Technologies used:

• Scikit‑learn  
• Pandas  
• Pathlib  
• Joblib  

The trained model is later loaded inside the **FastAPI inference service**.

---

# ⚡ FastAPI Prediction Service

The model is exposed as a **REST API** using **FastAPI**.

Main file:

src/api/main.py

Features:

• `/v1/predict` endpoint for predictions  
• `/health` endpoint for health checks  
• `/metrics` endpoint for Prometheus metrics  
• Automatic **Swagger UI documentation**  

Schemas for request validation are implemented with **Pydantic**:

src/api/schemas.py

Example request:

```json
{
  "tenure": 5,
  "monthly_charges": 75,
  "contract_type": "Month-to-month"
}
```

Swagger UI:

![API Docs](docs/screenshots/api-docs.png)

---

# 🗄 Database Layer

Predictions are stored in **PostgreSQL** for auditing and monitoring.

Database logic is implemented using:

• SQLAlchemy  
• Psycopg2

Key files:

src/db/database.py  
src/db/models.py  
src/db/crud.py

Stored fields:

• request_id  
• churn_probability  
• churn_label  
• latency_ms  
• timestamp

---

# 🐳 Containerized Infrastructure

The entire system runs inside **Docker containers**.

Defined in:

Dockerfile  
docker-compose.yml

Containers:

• churn-api  
• postgres database  
• prometheus  
• grafana  

Run locally:

docker compose up -d

---

# 📊 Monitoring & Observability

The ML service exposes metrics through **Prometheus**.

Metrics include:

• API request count  
• prediction volume  
• latency histograms  
• error rates

Metrics endpoint:

GET /metrics

![Metrics](docs/screenshots/metrics-endpoint.png)

---

# 📈 Grafana Dashboards

Example monitoring dashboards:

### Dashboard Overview

![Dashboard](docs/screenshots/dashboard-overview.png)

### Request Rate

![Request Rate](docs/screenshots/request-raterequest-rate.png)

### Prediction Volume

![Prediction Volume](docs/screenshots/predict-volume.png)

### Latency (p95)

![Latency](docs/screenshots/latency-p95.png)

### Error Rate

![Error](docs/screenshots/error-rate.png)

---

# ☸ Kubernetes Deployment

Kubernetes manifests are stored in:

k8s/

Resources include:

• API Deployment  
• PostgreSQL Deployment  
• Persistent Volume Claim  
• Kubernetes Secrets

Key files:

k8s/api/deployment.yaml  
k8s/postgres/deployment.yaml  
k8s/postgres/pvc.yaml  
k8s/postgres/secret.yaml

Run locally with Docker Desktop Kubernetes:

kubectl apply -f k8s/

---

# ☁ AWS Deployment

The system is deployed to **AWS EC2**.

Infrastructure used:

• EC2 instance (t3.micro)  
• AMI  
• Security Groups  
• Elastic IP  
• SSH access using `.pem` keypair  

Deployment flow:

GitHub → GitHub Actions → EC2 → Docker containers

---

# 🔄 CI/CD Pipeline

GitHub Actions automatically:

1. Builds Docker image
2. Pushes image to GitHub Container Registry
3. Deploys updated containers on EC2

Workflow file:

.github/workflows/deploy.yml

![CI/CD](docs/screenshots/github-actions-success.png)

---

# 🌍 Public Access

Public access configured using:

• DuckDNS domain  
• Nginx reverse proxy  
• HTTPS via Certbot TLS

![Domain](docs/screenshots/duckdns-domain.png)

---

# 🏗 System Architecture

![Architecture](docs/architecture/ml_churn_architecture_simple_aligned.png)

Flow:

User → FastAPI API → ML Model → PostgreSQL  
                              ↓  
                     Prometheus Metrics → Grafana Dashboards

---

# 📂 Project Structure

```
ml-churn-production
│
├── src/
│   ├── api/
│   ├── db/
│   └── ml/
│
├── docs/
│   ├── architecture/
│   └── screenshots/
│
├── k8s/
├── infra/prometheus/
├── .github/workflows/
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# 🎯 Engineering Concepts Demonstrated

✔ Machine Learning inference service  
✔ API design with FastAPI  
✔ Containerized ML deployment  
✔ Kubernetes orchestration  
✔ Monitoring with Prometheus  
✔ Visualization with Grafana  
✔ CI/CD automation  
✔ Cloud deployment (AWS EC2)

---

# 👨‍💻 Author

Mukesh Thenraj  
M.Sc Automation & Safety Engineering  
University of Duisburg‑Essen

GitHub:  
https://github.com/Mukeshthenraj
