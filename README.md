<div align="center">

# 🌾 AgriVision AI

### AI-Powered Crop Disease Detection for Indian Farmers

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Upload a crop leaf photo → Get instant disease diagnosis with treatment recommendations in **English, Hindi, and Marathi**.

[Features](#-features) · [Tech Stack](#-tech-stack) · [Quick Start](#-quick-start) · [API Docs](#-api-documentation) · [Architecture](#-architecture)

</div>

---

## 🎯 Problem

Indian agriculture loses **₹90,000+ crores annually** to crop diseases. Farmers in rural areas lack access to timely diagnosis and expert advice. AgriVision AI solves this by putting the power of AI in every farmer's pocket.

## 💡 Solution

AgriVision AI uses a **fine-tuned MobileNetV2** deep learning model to detect **38 crop diseases across 14 crops** from a single leaf photograph. It provides:

- ⚡ Instant diagnosis (< 2 seconds)
- 📊 Confidence scores and severity assessment
- 💊 Treatment recommendations (organic + chemical)
- 🛡️ Prevention tips
- 🗣️ Multilingual support (English, Hindi, Marathi)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Disease Detection** | Upload a leaf photo, get instant AI diagnosis |
| 📊 **Confidence Scoring** | Top-3 predictions with confidence percentages |
| ⚠️ **Severity Assessment** | High / Moderate / Low severity classification |
| 💊 **Treatment Advice** | Organic and chemical treatment recommendations |
| 🛡️ **Prevention Tips** | Actionable steps to prevent disease spread |
| 🗣️ **Multilingual** | Full UI and content in English, Hindi, Marathi |
| 📱 **Responsive** | Works on mobile, tablet, and desktop |
| 🔐 **User Accounts** | Sign up, track prediction history, analytics |
| 📈 **Analytics Dashboard** | Personal disease tracking and insights |
| 🐳 **Docker Ready** | One-command deployment with Docker |
| ☁️ **Cloud Deployable** | Ready for Google Cloud Run |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│           React Frontend (Vite + Tailwind)      │
│    Upload UI · Results · Dashboard · Auth        │
└─────────────────────┬───────────────────────────┘
                      │ REST API (HTTPS)
┌─────────────────────┴───────────────────────────┐
│              FastAPI Backend                      │
│  Routers · Schemas · Middleware · Auth (JWT)      │
├─────────────────────────────────────────────────┤
│           TensorFlow Inference Engine            │
│  MobileNetV2 · Pre-processing · Post-processing  │
├─────────────────────────────────────────────────┤
│               Data Layer                         │
│  Firebase Auth · Firestore · Disease KB          │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **ML** | TensorFlow 2.x, Keras, MobileNetV2 | Transfer learning for disease classification |
| **Backend** | FastAPI, Python 3.11, Pydantic | Async API with auto-generated docs |
| **Frontend** | React 18, Vite, Tailwind CSS, Framer Motion | Modern, responsive, animated UI |
| **Database** | Firebase Firestore | User data, prediction history |
| **Auth** | JWT + bcrypt | Secure authentication |
| **Container** | Docker, Docker Compose | Consistent dev/production environments |
| **Cloud** | Google Cloud Run | Serverless, auto-scaling deployment |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/agrivision-ai.git
cd agrivision-ai
```

### 2. Start the Backend
```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
> API docs available at: http://localhost:8000/api/docs

### 3. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```
> App available at: http://localhost:5173

### 4. Train the Model (Optional)
```bash
cd backend
# Download PlantVillage dataset to ./datasets/plantvillage/
python ml/train.py --data-dir ./datasets/plantvillage --epochs 25
```

### Docker (Recommended for Production)
```bash
docker compose up --build
```

---

## 📡 API Documentation

Once the backend is running, interactive API docs are available at:

| Docs | URL |
|------|-----|
| **Swagger UI** | http://localhost:8000/api/docs |
| **ReDoc** | http://localhost:8000/api/redoc |
| **OpenAPI JSON** | http://localhost:8000/api/openapi.json |

### Key Endpoints

```bash
# Health check
GET /api/health

# Predict disease (upload image)
POST /api/v1/predict
  - file: image (multipart/form-data)
  - language: en | hi | mr

# List supported crops
GET /api/v1/crops

# Get disease info
GET /api/v1/diseases/{disease_id}?language=en

# Auth
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me

# History & Analytics (authenticated)
GET /api/v1/history
GET /api/v1/analytics
```

### Sample Response
```json
{
  "success": true,
  "data": {
    "disease": "Tomato Late Blight",
    "crop": "Tomato",
    "confidence": 0.967,
    "severity": "high",
    "is_healthy": false,
    "top_predictions": [
      {"disease": "Tomato Late Blight", "confidence": 0.967},
      {"disease": "Tomato Early Blight", "confidence": 0.021},
      {"disease": "Tomato Healthy", "confidence": 0.008}
    ],
    "disease_info": {
      "description": "Late blight is a devastating disease...",
      "symptoms": ["Dark water-soaked lesions", "White fuzzy growth"],
      "treatment": {
        "organic": ["Remove infected plants", "Apply copper fungicide"],
        "chemical": ["Metalaxyl + Mancozeb @ 2.5g/L"]
      },
      "prevention": ["Use resistant varieties", "Avoid overhead irrigation"]
    },
    "processing_time_ms": 847
  }
}
```

---

## 📂 Project Structure

```
agrivision-ai/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Settings management
│   │   ├── routers/             # API endpoints
│   │   ├── schemas/             # Pydantic models
│   │   ├── services/            # Business logic
│   │   ├── core/                # Security, exceptions
│   │   └── middleware/          # Request processing
│   ├── ml/
│   │   ├── train.py             # Model training script
│   │   └── models/              # Saved .h5 models
│   ├── data/                    # Disease knowledge base
│   ├── tests/                   # Backend tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/               # Route pages
│   │   ├── components/          # Reusable components
│   │   ├── services/            # API client
│   │   └── i18n/                # Translations
│   ├── package.json
│   └── tailwind.config.js
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## 🧪 ML Model Details

| Metric | Value |
|--------|-------|
| **Architecture** | MobileNetV2 (Transfer Learning) |
| **Dataset** | PlantVillage (54,305 images) |
| **Classes** | 38 (14 crops × multiple diseases + healthy) |
| **Image Size** | 224 × 224 × 3 |
| **Validation Accuracy** | ~96% |
| **Inference Time** | < 200ms (CPU) |

### Supported Crops
Apple · Blueberry · Cherry · Corn · Grape · Orange · Peach · Pepper · Potato · Raspberry · Rice · Soybean · Squash · Strawberry · Tomato

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Your Name** — B.Tech AI/ML, D Y Patil Agriculture and Technical University, Talsande

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)

---

<div align="center">

**Built with 🌱 for Indian Agriculture**

*AgriVision AI — Because every farmer deserves access to expert plant pathology.*

</div>
