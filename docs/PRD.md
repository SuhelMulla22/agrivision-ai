# 📋 AgriVision AI — Product Requirements Document (PRD)

**Version:** 1.0  
**Author:** Senior Dev Team  
**Date:** July 2026  
**Status:** In Development  

---

## 1. Executive Summary

AgriVision AI is an AI-powered crop disease detection platform built for Indian farmers and agricultural students. Users upload a photo of a crop leaf, and the system instantly identifies the disease (if any) with confidence scores, severity assessment, and actionable treatment recommendations in English, Hindi, and Marathi.

This is not a demo — this is a **production-grade web application** with proper authentication, real-time inference, analytics dashboard, responsive UI, and cloud deployment.

---

## 2. Problem Statement

Indian agriculture loses **₹90,000+ crores annually** to crop diseases. Farmers in rural Maharashtra (including Kolhapur/Talsande region) face:
- Late disease detection — symptoms visible only when damage is severe
- No access to agricultural experts in remote areas
- Language barriers — most AI tools are English-only
- Cost — lab-based diagnosis is expensive and slow

**AgriVision AI solves all four.**

---

## 3. Target Users

| User | Need |
|------|------|
| **Farmers** | Quick disease diagnosis from phone camera, in Marathi/Hindi |
| **Agricultural Students** | Learn crop pathology through AI-assisted analysis |
| **Research Scholars** | Analyze disease patterns across regions and seasons |
| **Extension Workers** | Show farmers instant results during field visits |

---

## 4. Product Goals

| # | Goal | Success Metric |
|---|------|---------------|
| G1 | Accurate disease detection | ≥95% test accuracy on PlantVillage benchmark |
| G2 | Fast inference | <2 seconds from upload to result |
| G3 | Beautiful, responsive UI | Works on mobile, tablet, desktop |
| G4 | Multilingual support | English, Hindi, Marathi |
| G5 | Production-ready architecture | Dockerized, CI/CD, cloud-deployed |
| G6 | Accessible to farmers | Simple UX, minimal steps, visual results |

---

## 5. Technical Architecture

### 5.1 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │         React Frontend (Vite + Tailwind)        │    │
│  │  ┌──────────┐ ┌──────────┐ ┌────────────────┐  │    │
│  │  │  Upload   │ │ Results  │ │   Dashboard    │  │    │
│  │  │  Module   │ │  Page    │ │   (Analytics)  │  │    │
│  │  └──────────┘ └──────────┘ └────────────────┘  │    │
│  └──────────────────────┬──────────────────────────┘    │
│                         │ HTTPS (REST API)               │
├─────────────────────────┼───────────────────────────────┤
│                    API LAYER                             │
│  ┌──────────────────────┴──────────────────────────┐    │
│  │              FastAPI Backend                      │    │
│  │  ┌──────────┐ ┌──────────┐ ┌────────────────┐  │    │
│  │  │ Auth     │ │ Predict  │ │   Analytics    │  │    │
│  │  │ Router   │ │ Router   │ │   Router       │  │    │
│  │  └──────────┘ └──────────┘ └────────────────┘  │    │
│  │  ┌──────────┐ ┌──────────┐ ┌────────────────┐  │    │
│  │  │ Middleware│ │ Schemas  │ │   Services     │  │    │
│  │  └──────────┘ └──────────┘ └────────────────┘  │    │
│  └──────────────────────┬──────────────────────────┘    │
│                         │                                │
├─────────────────────────┼───────────────────────────────┤
│                    ML LAYER                              │
│  ┌──────────────────────┴──────────────────────────┐    │
│  │           TensorFlow Inference Engine            │    │
│  │  ┌──────────┐ ┌──────────┐ ┌────────────────┐  │    │
│  │  │  Model   │ │  Pre-    │ │   Post-        │  │    │
│  │  │  Loader  │ │  process │ │   process      │  │    │
│  │  └──────────┘ └──────────┘ └────────────────┘  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    DATA LAYER                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────┐   │
│  │ Firebase  │ │ Firebase │ │   Local Model        │   │
│  │ Auth      │ │ Firestore│ │   Storage (.h5)      │   │
│  └──────────┘ └──────────┘ └──────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Tech Stack Decision Matrix

| Layer | Technology | Why |
|-------|-----------|-----|
| **Frontend** | React 18 + Vite + Tailwind CSS + Framer Motion | Modern, fast, beautiful animations, industry standard |
| **Backend** | FastAPI (Python 3.11+) | Async, auto-docs, fast, Python ecosystem for ML |
| **ML Framework** | TensorFlow 2.x + Keras | Google's ML framework — perfect for GDG showcase |
| **ML Architecture** | MobileNetV2 (Transfer Learning) | Lightweight, fast inference, mobile-ready |
| **Database** | Firebase Firestore | NoSQL, real-time, free tier, Google ecosystem |
| **Auth** | Firebase Authentication | Google sign-in, email/password, free tier |
| **Storage** | Firebase Storage | For uploaded images, free tier |
| **i18n** | Custom translation service | English, Hindi, Marathi |
| **Containerization** | Docker + docker-compose | Production parity, easy deployment |
| **Deployment** | Google Cloud Run | Serverless, auto-scaling, pay-per-use, FREE tier |
| **CI/CD** | GitHub Actions | Free for public repos, integrates with GCP |
| **Testing** | Pytest (backend) + Vitest (frontend) | Industry standard |
| **API Docs** | FastAPI auto-generated (Swagger/ReDoc) | Zero effort, professional |

---

## 6. Feature Specification

### 6.1 MVP Features (v1.0)

#### F1: Image Upload & Prediction
- User uploads crop leaf image (JPG, PNG, WEBP)
- Max file size: 10MB
- Client-side image preview before upload
- Drag-and-drop support
- Real-time progress indicator during upload
- Returns: disease name, confidence %, severity level, affected crop

#### F2: Disease Information
- Disease name (localized)
- Description of the disease
- Symptoms to look for
- Causes
- **Treatment recommendations** (organic + chemical)
- Prevention tips
- All info in English / Hindi / Marathi

#### F3: Prediction History
- Logged-in users can view past predictions
- Timeline view with images
- Re-analyze old images
- Export history as CSV

#### F4: Analytics Dashboard
- Personal prediction statistics
- Most common diseases detected
- Crop health score trend over time
- Region-wise disease distribution (anonymized aggregate)

#### F5: User Authentication
- Email/Password sign-up
- Google Sign-In
- Protected routes
- User profile management

#### F6: Multilingual Support
- Language switcher (EN / HI / MR)
- All UI text translated
- Disease information in all 3 languages
- Auto-detect browser language

### 6.2 Post-MVP Features (v1.1+)
- Camera capture (live)
- Batch upload (multiple images)
- Community reports
- Expert consultation booking
- Weather-based disease risk alerts
- Mobile app (React Native / Flutter)

---

## 7. Supported Crops & Diseases

| Crop | Diseases | Healthy |
|------|----------|---------|
| **Rice** | Bacterial Blight, Blast, Brown Spot, Tungro | ✅ |
| **Wheat** | Rust (Yellow, Brown, Stripe), Septoria, Powdery Mildew | ✅ |
| **Cotton** | Bacterial Blight, Alternaria Leaf Spot, Verticillium Wilt | ✅ |
| **Tomato** | Early Blight, Late Blight, Leaf Mold, Bacterial Spot, Mosaic Virus, Yellow Leaf Curl | ✅ |
| **Potato** | Early Blight, Late Blight | ✅ |
| **Corn/Maize** | Northern Leaf Blight, Common Rust, Gray Leaf Spot, Cercospora | ✅ |
| **Grape** | Black Rot, Esca, Leaf Blight | ✅ |
| **Pepper** | Bacterial Spot | ✅ |
| **Cherry** | Powdery Mildew | ✅ |
| **Peach** | Bacterial Spot | ✅ |
| **Apple** | Apple Scab, Black Rot, Cedar Apple Rust | ✅ |
| **Soybean** | Various diseases | ✅ |
| **Squash** | Powdery Mildew | ✅ |
| **Strawberry** | Leaf Scorch | ✅ |

**Total: 14 crops, 38 classes (including healthy)**

---

## 8. ML Model Specification

### 8.1 Architecture
```
Input (224×224×3)
    ↓
MobileNetV2 (frozen, ImageNet weights)
    ↓
Global Average Pooling (1280 features)
    ↓
Dropout (0.3)
    ↓
Dense (256, ReLU)
    ↓
Batch Normalization
    ↓
Dropout (0.2)
    ↓
Dense (38, Softmax) → 38 disease classes
```

### 8.2 Training Configuration
| Parameter | Value |
|-----------|-------|
| Dataset | PlantVillage (54,305 images, 38 classes) |
| Image Size | 224 × 224 × 3 |
| Batch Size | 32 |
| Epochs | 25 (with early stopping) |
| Learning Rate | 1e-3 (Adam) → 1e-5 (fine-tune last 20 layers) |
| Augmentation | Rotation, flip, zoom, brightness, contrast |
| Validation Split | 20% |
| Target Accuracy | ≥95% validation accuracy |

### 8.3 Inference Pipeline
```
Raw Image (any size)
    ↓
Resize to 224×224
    ↓
Normalize (0-1)
    ↓
Expand dims (batch)
    ↓
Model predict (softmax)
    ↓
Top-3 predictions with confidence
    ↓
Map class → disease info (from knowledge base)
    ↓
Translate to user's language
    ↓
Return JSON response (< 2 seconds total)
```

---

## 9. API Specification

### 9.1 Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/predict` | Optional | Upload image, get prediction |
| GET | `/api/v1/diseases/{crop}` | No | Get disease info for a crop |
| GET | `/api/v1/crops` | No | List all supported crops |
| POST | `/api/v1/auth/register` | No | Register new user |
| POST | `/api/v1/auth/login` | No | Login user |
| GET | `/api/v1/auth/me` | Yes | Get current user profile |
| GET | `/api/v1/history` | Yes | Get prediction history |
| GET | `/api/v1/analytics` | Yes | Get user analytics |
| GET | `/api/v1/health` | No | Health check |

### 9.2 Sample Response — `/api/v1/predict`

```json
{
  "success": true,
  "data": {
    "prediction": {
      "disease": "Tomato Late Blight",
      "disease_id": "tomato_late_blight",
      "crop": "Tomato",
      "confidence": 0.967,
      "severity": "high",
      "is_healthy": false
    },
    "top_predictions": [
      {"disease": "Tomato Late Blight", "confidence": 0.967},
      {"disease": "Tomato Early Blight", "confidence": 0.021},
      {"disease": "Tomato Healthy", "confidence": 0.008}
    ],
    "disease_info": {
      "description": "Late blight is a potentially devastating disease...",
      "symptoms": ["Dark, water-soaked lesions", "White fuzzy growth on undersides"],
      "causes": ["Phytophthora infestans fungus", "Cool, wet weather"],
      "treatment": {
        "organic": ["Remove infected plants", "Apply copper-based fungicide"],
        "chemical": ["Mancozeb 75% WP @ 2g/L", "Metalaxyl + Mancozeb"]
      },
      "prevention": ["Use resistant varieties", "Ensure good air circulation"]
    },
    "language": "en",
    "processing_time_ms": 847
  }
}
```

---

## 10. UI/UX Design Principles

### 10.1 Design System
- **Color Palette:** 
  - Primary: `#16a34a` (Green — agriculture)
  - Secondary: `#059669` (Emerald)
  - Accent: `#f59e0b` (Amber — warning/severity)
  - Background: `#f8fafc` (Light gray)
  - Dark: `#0f172a` (Navy)
- **Typography:** Inter (body), Poppins (headings)
- **Border Radius:** Rounded corners (0.75rem default)
- **Shadows:** Soft, layered shadows for depth
- **Animations:** Subtle, purposeful (Framer Motion)

### 10.2 Pages

| Page | Route | Description |
|------|-------|-------------|
| Landing | `/` | Hero section, how it works, stats, CTA |
| Upload | `/analyze` | Drag-drop upload, instant results |
| Results | `/results/:id` | Full disease report with treatment |
| History | `/history` | Past predictions timeline |
| Dashboard | `/dashboard` | Analytics & insights |
| Login | `/auth/login` | Sign in |
| Register | `/auth/register` | Sign up |
| About | `/about` | Team, mission, tech stack |

---

## 11. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| **Performance** | API response < 2s, Frontend load < 3s |
| **Availability** | 99.5% uptime (Cloud Run SLA) |
| **Security** | Input validation, rate limiting, CORS, helmet headers |
| **Accessibility** | WCAG 2.1 AA compliance |
| **SEO** | Meta tags, Open Graph, semantic HTML |
| **Monitoring** | Structured logging, error tracking |
| **Testing** | ≥80% backend test coverage |

---

## 12. Project Structure

```
agrivision-ai/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Backend tests
│       └── deploy.yml                # Deploy to Cloud Run
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry
│   │   ├── config.py                 # Settings/env vars
│   │   ├── dependencies.py           # Dependency injection
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py            # Prediction endpoints
│   │   │   ├── auth.py               # Auth endpoints
│   │   │   ├── diseases.py           # Disease info endpoints
│   │   │   ├── history.py            # History endpoints
│   │   │   └── analytics.py          # Analytics endpoints
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── prediction.py         # Pydantic models
│   │   │   ├── auth.py
│   │   │   ├── disease.py
│   │   │   └── common.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── model_service.py      # TF model loading & inference
│   │   │   ├── disease_service.py    # Disease knowledge base
│   │   │   ├── translation.py        # i18n service
│   │   │   └── firebase_service.py   # Firebase operations
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── rate_limit.py
│   │   │   ├── logging.py
│   │   │   └── cors.py
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── security.py           # JWT, password hashing
│   │       └── exceptions.py         # Custom exceptions
│   ├── ml/
│   │   ├── train.py                  # Model training script
│   │   ├── evaluate.py               # Model evaluation
│   │   ├── preprocess.py             # Data preprocessing
│   │   └── models/                   # Saved .h5 / .tflite models
│   ├── data/
│   │   ├── disease_knowledge.json    # Disease info (EN/HI/MR)
│   │   └── class_mapping.json        # Class index → disease name
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_predict.py
│   │   ├── test_auth.py
│   │   └── test_diseases.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── index.css                 # Global styles + Tailwind
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   └── Layout.jsx
│   │   │   ├── upload/
│   │   │   │   ├── DropZone.jsx
│   │   │   │   ├── ImagePreview.jsx
│   │   │   │   └── UploadProgress.jsx
│   │   │   ├── results/
│   │   │   │   ├── PredictionCard.jsx
│   │   │   │   ├── DiseaseInfo.jsx
│   │   │   │   ├── ConfidenceBar.jsx
│   │   │   │   └── TreatmentCard.jsx
│   │   │   ├── dashboard/
│   │   │   │   ├── StatsCards.jsx
│   │   │   │   ├── DiseaseChart.jsx
│   │   │   │   └── HistoryTimeline.jsx
│   │   │   └── common/
│   │   │       ├── Button.jsx
│   │   │       ├── Card.jsx
│   │   │       ├── Loading.jsx
│   │   │       ├── LanguageSwitcher.jsx
│   │   │       └── ProtectedRoute.jsx
│   │   ├── pages/
│   │   │   ├── Landing.jsx
│   │   │   ├── Analyze.jsx
│   │   │   ├── Results.jsx
│   │   │   ├── History.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   └── About.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── usePrediction.js
│   │   │   └── useLanguage.js
│   │   ├── services/
│   │   │   ├── api.js                # Axios instance
│   │   │   ├── auth.js               # Auth API calls
│   │   │   └── prediction.js         # Prediction API calls
│   │   ├── context/
│   │   │   ├── AuthContext.jsx
│   │   │   └── LanguageContext.jsx
│   │   ├── i18n/
│   │   │   ├── en.json
│   │   │   ├── hi.json
│   │   │   └── mr.json
│   │   └── utils/
│   │       ├── constants.js
│   │       └── helpers.js
│   ├── public/
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   └── .env.example
├── docker-compose.yml
├── Makefile
├── .gitignore
├── LICENSE
└── README.md
```

---

## 13. Milestones

| Milestone | Deliverable | Timeline |
|-----------|-------------|----------|
| M1 | Project setup, structure, configs | Day 1 |
| M2 | ML model trained & evaluated | Day 2-3 |
| M3 | Backend API complete + tested | Day 4-6 |
| M4 | Frontend complete + responsive | Day 7-10 |
| M5 | Integration + Docker + deployment | Day 11-12 |
| M6 | Polish, README, GitHub profile | Day 13-14 |

---

*This PRD is our contract. Every line of code we write traces back to a requirement here.*
