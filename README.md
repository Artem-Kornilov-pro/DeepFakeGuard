# 🛡️ DeepFakeGuard

**Privacy-Preserving Deepfake Detection with Federated Learning**

_A distributed system that detects AI-generated videos without compromising user privacy._

---

## 📖 Overview

DeepFakeGuard is an end-to-end machine learning platform for detecting deepfake videos. Unlike traditional centralized solutions, it uses **federated learning** — the model trains across distributed clients without ever collecting raw video data on a central server. Only encrypted weight updates are shared.

### Why this project is unique

- **Federated Learning with Flower** — distributed training across multiple clients, each holding private video data
- **Differential Privacy** — noise injection to weight updates prevents data leakage even from gradients
- **Vision Transformer backbone** — state-of-the-art architecture for detecting subtle manipulation artifacts
- **Temporal analysis** — processes video frame sequences, not just static images
- **Full MLOps pipeline** — experiment tracking, model versioning, automated evaluation
- **Production-ready API** — FastAPI with async support, Celery for heavy inference tasks

---

## 🧠 Core Components

### 1. Video Analysis Engine

- **Vision Transformer (ViT)** or **XceptionNet** backbone for frame-level feature extraction
- **Temporal fusion** — LSTM/Transformer over frame sequences to catch inter-frame inconsistencies
- Detects: facial manipulation, unnatural blinking, compression artifacts, boundary inconsistencies

### 2. Federated Learning System

- **Flower framework** for orchestrating training rounds
- Each client trains locally on private video data
- Only model weight updates (gradients) are sent to the server — never raw videos
- **Differential Privacy** via DP-SGD: noise added to gradients before transmission
- **Secure Aggregation** — server combines updates without seeing individual contributions

### 3. API Server

- **FastAPI** REST endpoints for:
  - Video upload and inference requests
  - Client registration and authentication
  - Model metrics and dashboard data
- **Celery** task queue for long-running video processing
- **Redis** for caching and federated round coordination
- **WebSocket** support for streaming inference progress

### 4. Data & Storage

- **PostgreSQL** — users, client metadata, inference logs
- **MinIO / S3** — uploaded videos (encrypted at rest)
- **Redis** — session state, federated round locks, rate limiting

### 5. MLOps & Monitoring

- **MLflow** — experiment tracking, model registry, versioning
- **Evidently AI** — data drift detection on incoming video distributions
- **Prometheus + Grafana** — system metrics, inference latency, federated round progress
- **GitHub Actions CI/CD** — automated testing, model evaluation, Docker builds

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- NVIDIA GPU (optional, for local training)

### Installation

```bash
# Clone the repository
git clone https://github.com/Artem-Kornilov-pro/DeepFakeGuard.git
cd DeepFakeGuard

# Set up environment
cp .env.example .env
docker-compose up -d --build

# Run database migrations
docker-compose exec api alembic upgrade head

# Start the API server
docker-compose exec api uvicorn src.main:app --host 0.0.0.0 --port 8000

# Start a federated client (on client machine)
docker-compose exec client python -m src.client --server-address server:8080
Quick Test
bash
# Upload a video for inference
curl -X POST http://localhost:8000/api/v1/predict \
  -F "video=@test_video.mp4" \
  -F "model_version=v1.2.0"

# Response
{
  "prediction": "fake",
  "confidence": 0.94,
  "processing_time_ms": 1240,
  "model_version": "v1.2.0"
}
```
📡 API Endpoints
Method	Endpoint	Description
POST	/api/v1/predict	Upload video for deepfake detection
GET	/api/v1/predict/{task_id}	Get inference result by task ID
POST	/api/v1/clients/register	Register a new federated client
GET	/api/v1/model/status	Current global model metrics
GET	/api/v1/dashboard	Federated training dashboard data
GET	/docs	Swagger UI documentation
🧪 Dataset & Training
Datasets used
FaceForensics++ — 1000+ original and manipulated videos

DFDC (DeepFake Detection Challenge) — 100K+ clips

Celeb-DF — high-quality celebrity deepfakes

Custom augmentation — compression, blur, noise to simulate real-world conditions

Training modes
Centralized baseline — train on full dataset for performance comparison

Federated (IID) — evenly distributed data across clients

Federated (non-IID) — realistic scenario with skewed client data distributions


🛠️ Tech Stack
Layer	Technology
ML Framework	PyTorch 2.x
Vision Models	Vision Transformer, XceptionNet, EfficientNet
Federated Learning	Flower, DP-SGD (Opacus)
API Server	FastAPI, Uvicorn
Task Queue	Celery, Redis
Database	PostgreSQL, SQLAlchemy 2.0
Object Storage	MinIO (S3-compatible)
Experiment Tracking	MLflow
Drift Monitoring	Evidently AI
Metrics	Prometheus, Grafana
CI/CD	GitHub Actions
Containers	Docker, Docker Compose
Testing	pytest, pytest-asyncio, pytest-mock
📄 License
MIT — see LICENSE file.
