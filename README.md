\# 🚀 ML Churn Prediction Production System



Production-ready Machine Learning API built with \*\*FastAPI\*\*, containerized using \*\*Docker\*\*, deployed with \*\*Kubernetes\*\*, automated with \*\*GitHub Actions CI/CD\*\*, and monitored using \*\*Prometheus + Grafana\*\* on \*\*AWS EC2\*\*.



This project demonstrates how to take a \*\*machine learning model from training to production infrastructure\*\*.



\---



\# 📌 Project Goal



The goal of this project is to simulate a \*\*real production ML system\*\* that includes:



\* ML model training pipeline

\* REST API for predictions

\* containerized deployment

\* Kubernetes orchestration

\* CI/CD pipeline

\* monitoring and observability

\* cloud deployment



\---



\# 🧠 Machine Learning Problem



Dataset: \*\*Telco Customer Churn\*\*



The model predicts whether a telecom customer will \*\*leave the service (churn)\*\*.



Output example:



```

{

&#x20; "churn\_probability": 0.69,

&#x20; "churn\_label": 1

}

```



\---



\# 🏗️ System Architecture



!\[Architecture](docs/architecture/ml\_churn\_architecture\_simple\_aligned.png)



\---



\# ⚙️ Tech Stack



\### Machine Learning



\* Python

\* Scikit-learn

\* Pandas

\* Joblib



\### API Layer



\* FastAPI

\* Uvicorn

\* Pydantic



\### Infrastructure



\* Docker

\* Docker Compose

\* Kubernetes (Docker Desktop)



\### Data Storage



\* PostgreSQL



\### Monitoring



\* Prometheus

\* Grafana



\### DevOps



\* Git

\* GitHub

\* GitHub Actions CI/CD



\### Cloud



\* AWS EC2

\* DuckDNS domain



\---



\# 📂 Project Structure



```

ml-churn-production

│

├── src

│   ├── api

│   │   └── main.py

│   ├── model

│   └── services

│

├── data

│

├── infra

│   └── prometheus

│

├── k8s

│

├── docs

│   ├── architecture

│   └── screenshots

│

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

└── README.md

```



\---



\# 🔁 Machine Learning Pipeline



1️⃣ Load dataset

2️⃣ Data preprocessing

3️⃣ Train classification model

4️⃣ Save model artifact

5️⃣ Serve model via API



\---



\# 🌐 API Endpoints



\### Health Check



```

GET /health

```



Example response:



```

{

&#x20; "status": "ok"

}

```



\---



\### Prediction Endpoint



```

POST /predict

```



Example request:



```

{

&#x20;"tenure": 12,

&#x20;"monthly\_charges": 70,

&#x20;"contract\_type": "Month-to-month"

}

```



Example response:



```

{

&#x20;"churn\_probability": 0.69,

&#x20;"churn\_label": 1

}

```



\---



\### Metrics Endpoint (Prometheus)



```

GET /metrics

```



Used for monitoring request performance.



\---



\# 📊 Monitoring Dashboard



The API is monitored using \*\*Prometheus and Grafana\*\*.



\### System Metrics Overview



!\[Dashboard](docs/screenshots/dashboard-overview.png)



\---



\### Request Rate



!\[Request Rate](docs/screenshots/request-rate.png)



\---



\### Prediction Volume



!\[Prediction Volume](docs/screenshots/predict-volume.png)



\---



\### Latency p95



!\[Latency](docs/screenshots/latency-p95.png)



\---



\### Error Rate



!\[Error Rate](docs/screenshots/error-rate.png)



\---



\# 🐳 Docker Deployment



Build containers:



```

docker compose build

```



Start services:



```

docker compose up -d

```



Services started:



\* FastAPI ML API

\* PostgreSQL database

\* Prometheus

\* Grafana



\---



\# ☸️ Kubernetes Deployment



Deploy application:



```

kubectl apply -f k8s/

```



Check services:



```

kubectl get svc

```



Forward API locally:



```

kubectl port-forward service/churn-api 8000:8000

```



\---



\# ☁️ AWS Deployment



The system is deployed on:



\*\*AWS EC2\*\*



Components deployed:



\* Docker containers

\* API service

\* monitoring stack



Public access is provided via \*\*DuckDNS domain\*\*.



\---



\# 🔄 CI/CD Pipeline



CI/CD is implemented using \*\*GitHub Actions\*\*.



Pipeline automatically:



1️⃣ builds Docker image

2️⃣ connects to EC2

3️⃣ deploys latest version



Example workflow:



!\[CI/CD](docs/screenshots/github-actions-success.png)



\---



\# 📈 Observability Stack



Monitoring stack:



```

API → Prometheus → Grafana

```



Prometheus collects:



\* request rate

\* request latency

\* error rate



Grafana visualizes system performance.



\---



\# 🧪 Example Prediction



Example curl request:



```

curl -X POST http://localhost:8000/predict \\

\-H "Content-Type: application/json" \\

\-d '{

"tenure": 12,

"monthly\_charges": 70

}'

```



\---



\# 📚 Key Skills Demonstrated



This project demonstrates production-level skills in:



\* Machine Learning deployment

\* MLOps

\* Docker containerization

\* Kubernetes orchestration

\* CI/CD automation

\* Monitoring and observability

\* Cloud infrastructure



\---



\# 👨‍💻 Author



Mukesh Thenraj



M.Sc. Automation \& Safety Engineering

University of Duisburg-Essen



GitHub

https://github.com/Mukeshthenraj



