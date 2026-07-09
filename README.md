<div align="center">

# 🌾 AgriVision AI

### 3-Tier Hybrid Universal AI Crop Disease Detection for Indian Farmers

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Supabase](https://img.shields.io/badge/Supabase-Database-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Frontend-000000?style=for-the-badge&logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Render-Backend-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Upload a crop leaf photo → Get instant universal disease diagnosis with organic and chemical treatment recommendations in **English, Hindi, and Marathi**.

[Features](#-features) · [Architecture](#-architecture) · [Tech Stack](#-tech-stack) · [Quick Start](#-quick-start) · [API Docs](#-api-documentation) · [Deployment](#-deployment)

</div>

---

## 🎯 Problem

Indian agriculture loses **₹90,000+ crores annually** to crop diseases. Farmers in rural areas lack access to timely diagnosis and expert advice. AgriVision AI solves this by putting the power of state-of-the-art cloud and offline edge Artificial Intelligence in every farmer's pocket.

## 💡 Solution: The 3-Tier AI Cascade

AgriVision AI uses a unique, resilient **three-tiered cascade architecture** to diagnose crop leaves:

1. **Tier 1 (Gemini 2.5 Flash Vision API)**: Analyzes the image using Google's cloud vision model for universal crop support and zero-shot disease identification.
2. **Tier 2 (OpenRouter Vision API Fallback)**: If Gemini API limits are hit, cascades immediately to secondary large vision models to ensure continuous uptime.
3. **Tier 3 (Local TF MobileNetV2 Classifier)**: If internet connectivity is lost or upstream APIs fail, runs inference locally using a fine-tuned MobileNetV2 model detecting 38 classes across 14 crops.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Disease Detection** | Upload a leaf photo, get instant universal AI diagnosis in <2s |
| 📊 **Confidence Scoring** | Visual metrics showing diagnosis reliability |
| ⚠️ **Severity Assessment** | High / Moderate / Low severity classification |
| 💊 **Treatment Advice** | Organic and chemical treatment recommendations |
| 🛡️ **Prevention Tips** | Actionable steps to prevent disease spread |
| 🗣️ **Multilingual Support** | Full UI and translation in English, Hindi, and Marathi |
| 👤 **User Profile Page** | Unified profile details (Name, Email, Location) with personal analytics |
| 📈 **Analytics Dashboard** | Premium charts displaying scan trends, crop distribution, and severity donut |
| 📜 **Clickable History** | View previous diagnostic records inside animated modal popovers |
| 🚫 **Wildcard Routing** | Themed 404 page ("Page Not Found") for invalid URL fallbacks |
| 🐳 **Docker Ready** | One-command local containerization with Docker Compose |

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│           React Frontend (Vite + Tailwind)             │
│   Upload UI · Visual Dashboard · History · Profile     │
└───────────────────────────┬────────────────────────────┘
                            │ REST API (HTTPS + JWT)
┌───────────────────────────┴────────────────────────────┐
│                    FastAPI Backend                     │
│      Routers · Schemas · Security Headers · Auth       │
├───────────────────────────┬────────────────────────────┤
│   Universal AI Engine     │  Local Classifier (TF)     │
│   Gemini 2.5 / OpenRouter │  MobileNetV2 (Offline)     │
└───────────────────────────┼────────────────────────────┘
                            │ DB Clients (RLS Enabled)
┌───────────────────────────┴────────────────────────────┐
│             Supabase Cloud Infrastructure             │
│     User Database · Blob Storage · Auth Management     │
└────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **AI/ML** | Gemini 2.5 Flash, TensorFlow 2.x, MobileNetV2 | Hybrid vision APIs & offline edge classifier |
| **Backend** | FastAPI, Python 3.11, Pydantic, Uvicorn | Async REST API with automatic security headers |
| **Frontend** | React 18, Vite, Tailwind CSS, Framer Motion | Animated, responsive modern user experience |
| **Charts** | Recharts | Premium custom gradient bar charts & donut distributions |
| **Database** | Supabase (PostgreSQL) | User database records guarded by Row-Level Security (RLS) |
| **Storage** | Supabase Storage | Secure blob bucket storage for uploaded leaf snapshots |
| **Auth** | JWT + bcrypt | Secure session management & route authentication |
| **Container** | Docker, Docker Compose | Consistent local and staging docker runs |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### 1. Clone the repository
```bash
git clone https://github.com/SuhelMulla22/agrivision-ai.git
cd agrivision-ai
```

### 2. Start the Backend
```bash
cd backend
# Create virtual environment and install packages
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On Linux/macOS
pip install -r requirements.txt

# Create .env from example and fill in Supabase and Gemini keys
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
> API docs available at: http://127.0.0.1:8000/docs

### 3. Start the Frontend
```bash
cd frontend
# Install dependencies
npm install

# Start Vite server (runs on port 5176 to avoid local caching conflicts)
npm run dev
```
> App available at: http://localhost:5176

---

## 📡 API Documentation

Interactive API documents are available at:

| Docs | URL |
|------|-----|
| **Swagger UI** | http://127.0.0.1:8000/docs |
| **ReDoc** | http://127.0.0.1:8000/redoc |
| **OpenAPI JSON** | http://127.0.0.1:8000/openapi.json |

### Key Endpoints

```bash
# Health check
GET /api/health

# Predict disease (upload image - Requires auth token)
POST /api/v1/predict
  - file: image (multipart/form-data)
  - language: en | hi | mr

# Auth
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me

# History & Analytics (Requires auth token)
GET /api/v1/history
GET /api/v1/analytics
```

---

## ☁️ Deployment (Free Lifetime Setup)

Refer to the production configuration guidelines for hosting this stack at zero cost:

### 1. Backend (Render)
- Deploy your `backend` directory to **Render Web Services**.
- Since Render free tier offers 512MB RAM, set the environment variable:
  `SKIP_TF_LOAD` = `true`
  *This disables loading local TensorFlow into memory, keeping the server footprint under 80MB. The backend will route all predictions through Gemini Cloud API.*
- Configure your `GEMINI_API_KEY`, `SUPABASE_URL`, and `SUPABASE_ANON_KEY`.

### 2. Frontend (Vercel)
- Deploy your `frontend` directory to **Vercel**.
- Add the `VITE_API_URL` pointing to your Render backend URL, and add the Supabase URL/key.

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Suhel Mulla** — B.Tech AI/ML, D Y Patil Agriculture and Technical University, Talsande

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/suhelmulla22)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SuhelMulla22)

---

<div align="center">

**Built with 🌱 for Indian Agriculture**

*AgriVision AI — Because every farmer deserves access to expert plant pathology.*

</div>
