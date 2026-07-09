# AgriVision AI — Production Deployment Guide

This guide walks you through deploying **AgriVision AI** to the internet using industry-standard free hosting platforms.

---

## 🏗️ Architecture Overview
*   **Frontend**: React (SPA) hosted on **Vercel** or **Netlify** (Free tier, global CDN).
*   **Backend**: FastAPI hosted on **Render** (Free tier, containerized or python service).
*   **Database & Storage**: PostgreSQL & Blob Storage hosted on **Supabase** (Free tier).

---

## 📦 Phase 1: Database Setup (Supabase)
Your current Supabase database is already active and configured. Make sure you have the following credentials from the **Supabase Dashboard** (`Project Settings` → `API`):
1.  **Project URL**: e.g., `https://your-project-id.supabase.co`
2.  **Anon Public Key**: Used by both frontend and backend for database client operations.

---

## 🚀 Phase 2: Deploy Backend to Render (Free Web Service)

Render is a cloud hosting platform that can build and run Docker containers or Python services directly from your GitHub repository.

### Step 1: Create a Render Account
1.  Go to [render.com](https://render.com/) and sign up (link your GitHub account).
2.  Click **New +** → **Web Service**.

### Step 2: Connect Repository & Configure Service
1.  Connect your GitHub repository containing the AgriVision AI codebase.
2.  Set the following configuration parameters:
    *   **Name**: `agrivision-backend`
    *   **Region**: Select the region closest to your target users (e.g., Singapore for India).
    *   **Branch**: `main`
    *   **Root Directory**: `backend`
    *   **Runtime**: `Python 3` (or choose `Docker` since the repository has a `Dockerfile`!)
        *   *Recommendation*: Choosing **Docker** is highly recommended as Render will read our optimized multi-stage `Dockerfile` automatically.
    *   **Instance Type**: `Free`

### Step 3: Add Environment Variables
Under the **Environment** tab, click **Add Environment Variable** and configure these settings:
*   `ENVIRONMENT` = `production`
*   `DEBUG` = `false`
*   `SECRET_KEY` = `[GENERATE_A_RANDOM_LONG_SECRET]` (Do not use default; use a strong random string)
*   `SUPABASE_URL` = `[YOUR_SUPABASE_PROJECT_URL]`
*   `SUPABASE_ANON_KEY` = `[YOUR_SUPABASE_ANON_KEY]`
*   `GEMINI_API_KEY` = `[YOUR_GEMINI_API_KEY]`
*   `OPENROUTER_API_KEY` = `[YOUR_OPENROUTER_API_KEY]`
*   `CORS_ORIGINS` = `https://your-app-name.vercel.app` (You will get this URL in the next phase)
*   `SKIP_TF_LOAD` = `true` (Crucial for Render Free Tier to bypass local TensorFlow loading and prevent Out-of-Memory crashes)

Click **Create Web Service**. Render will now build and launch the API!

---

## 🎨 Phase 3: Deploy Frontend to Vercel (Free Static Site)

Vercel provides static site hosting with automatic builds when you push changes to GitHub.

### Step 1: Create a Vercel Account
1.  Go to [vercel.com](https://vercel.com) and log in using your GitHub account.
2.  Click **Add New** → **Project**.

### Step 2: Import Project
1.  Select your GitHub repository.
2.  Configure the build settings:
    *   **Framework Preset**: `Vite`
    *   **Root Directory**: `frontend`
    *   **Build Command**: `npm run build`
    *   **Output Directory**: `dist`

### Step 3: Configure Environment Variables
Expand the **Environment Variables** section and add the following keys:
*   `VITE_API_URL` = `https://your-render-service.onrender.com` (Use the URL Render generated for your backend service)
*   `VITE_SUPABASE_URL` = `[YOUR_SUPABASE_PROJECT_URL]`
*   `VITE_SUPABASE_ANON_KEY` = `[YOUR_SUPABASE_ANON_KEY]`

Click **Deploy**. Vercel will build and launch your application, giving you a public URL (e.g., `https://agrivision-ai.vercel.app`).

> [!IMPORTANT]
> Once Vercel gives you your frontend URL, remember to go back to your **Render Web Service Settings** and update the `CORS_ORIGINS` variable to match your Vercel URL! This ensures the frontend has permission to make API calls to your backend.
