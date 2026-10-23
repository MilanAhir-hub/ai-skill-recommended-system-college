# Deployment Architecture & Execution Plan

This guide outlines the production deployment strategy for **CareerCompass AI**:
- **Backend (Flask + SQLite API)** deployed on **Render** (Free Web Service)
- **Frontend (React + Vite + Tailwind CSS)** deployed on **Vercel** (Global Edge CDN)

---

## 🏗️ Production Architecture

```
  ┌─────────────────────────────────────────────────────────┐
  │                         USERS                           │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────────┐
        │              VERCEL (Frontend)               │
        │     https://careercompass-ai.vercel.app      │
        │  - React 19 + Vite SPA                      │
        │  - Global Edge CDN & SSL                     │
        │  - Client Routing (vercel.json)              │
        └──────────────────────┬───────────────────────┘
                               │
                               │ HTTPS / JSON REST API
                               │ (VITE_API_BASE_URL)
                               ▼
        ┌──────────────────────────────────────────────┐
        │              RENDER (Backend)                │
        │   https://careercompass-backend.onrender.com │
        │  - Python 3 + Gunicorn WSGI Server           │
        │  - Flask REST API + CORS enabled             │
        │  - SQLite Database Storage (users)           │
        └──────────────────────────────────────────────┘
```

---

## 📋 Pre-Deployment Checklist

| Item | Location | Status | Purpose |
| :--- | :--- | :--- | :--- |
| **Gunicorn WSGI** | [requirements.txt](file:///c:/Users/Milan%20Gagiya/Documents/PROJECT%20RESUME/ai-skill-recommended-system-college/requirements.txt) | Ready | Production WSGI server for Render |
| **CORS Support** | [app.py](file:///c:/Users/Milan%20Gagiya/Documents/PROJECT%20RESUME/ai-skill-recommended-system-college/app.py) | Ready | Permits Vercel frontend requests without CORS errors |
| **Dynamic DB Path** | [database.py](file:///c:/Users/Milan%20Gagiya/Documents/PROJECT%20RESUME/ai-skill-recommended-system-college/database.py) | Ready | Reads `DB_PATH` from environment variables |
| **Render Blueprint** | [render.yaml](file:///c:/Users/Milan%20Gagiya/Documents/PROJECT%20RESUME/ai-skill-recommended-system-college/render.yaml) | Ready | Infrastructure-as-code configuration for Render |
| **Vercel SPA Rewrites**| [frontend/vercel.json](file:///c:/Users/Milan%20Gagiya/Documents/PROJECT%20RESUME/ai-skill-recommended-system-college/frontend/vercel.json) | Ready | Prevents 404s on browser refresh |
| **Dynamic API Base URL**| [frontend/src/services/api.js](file:///c:/Users/Milan%20Gagiya/Documents/PROJECT%20RESUME/ai-skill-recommended-system-college/frontend/src/services/api.js) | Ready | Connects to `VITE_API_BASE_URL` |

---

## 🚀 Phase 1: Push Code to GitHub

1. Initialize git in the project root (if not already done):
   ```bash
   git init
   git add .
   git commit -m "feat: complete CareerCompass AI with Claude warm editorial design"
   ```
2. Create a new repository on [GitHub](https://github.com/new).
3. Push your repository:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```

---

## 🐍 Phase 2: Deploy Backend to Render

### Option A: Standard Render Web Service Setup (Recommended)
1. Go to **[dashboard.render.com](https://dashboard.render.com/)** and log in.
2. Click **New +** $\rightarrow$ select **Web Service**.
3. Choose **Build and deploy from a Git repository** $\rightarrow$ click **Next**.
4. Connect your GitHub account and select your repository.
5. Fill in the deployment settings:
   - **Name**: `careercompass-backend` (or your choice)
   - **Region**: Choose the closest region (e.g., *Singapore*, *Frankfurt*, *Oregon*)
   - **Branch**: `main`
   - **Root Directory**: Leave blank (uses repo root `.`)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: `Free`
6. Under **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.9`
   - `FLASK_ENV`: `production`
7. Click **Create Web Service**.
8. Wait 1–2 minutes for the build to finish. Once live, copy your service URL:
   `https://careercompass-backend.onrender.com`
9. **Test Your Backend**: Open `https://careercompass-backend.onrender.com/` in your browser. You should see:
   ```json
   {
     "status": "online",
     "message": "AI-Powered Personalized Career and Skill Recommendation API is running"
   }
   ```

---

## ⚡ Phase 3: Deploy Frontend to Vercel

1. Go to **[vercel.com](https://vercel.com/)** and log in with GitHub.
2. Click **Add New...** $\rightarrow$ select **Project**.
3. Select your GitHub repository and click **Import**.
4. Configure the project:
   - **Project Name**: `careercompass-ai`
   - **Framework Preset**: `Vite` (automatically detected)
   - **Root Directory**: Click **Edit** $\rightarrow$ select **`frontend`** $\rightarrow$ click **Continue**.
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `dist` (default)
5. Under **Environment Variables**, add:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: Your live Render backend URL from Phase 2:
     `https://careercompass-backend.onrender.com`
     *(Note: do not include a trailing slash)*
6. Click **Deploy**.
7. Vercel will build the React SPA in ~30 seconds and provide a production domain:
   `https://careercompass-ai.vercel.app`

---

## 🔍 Phase 4: Production Verification & Testing

Once both services are deployed:
1. Open your Vercel URL: `https://careercompass-ai.vercel.app`.
2. Look at the top navigation bar:
   - Verify that the status pill displays **Engine Online** with a green pulse dot.
3. Click **Find My Career**.
4. Fill in:
   - Name: `Milan Gagiya`
   - Degree: `Bachelor of Technology (B.Tech / B.E.) in Computer Science / IT`
   - Skills: `Python`, `SQL`, `Git`, `Machine Learning`
   - Interests: `Artificial Intelligence`, `Machine Learning`
   - Goal: `AI/ML Engineer`
5. Click **Generate Recommendations**.
6. Verify:
   - Profile is saved to the SQLite database on Render.
   - The dashboard displays the **Top 3 Recommended Careers**.
   - The visual progress bar, 50%/30%/20% score breakdown, and dark technical roadmap expander work smoothly.
7. Refresh the page to verify that `sessionStorage` maintains the active profile recommendations.

---

## 💡 Free Tier Considerations & Optimizations

### 1. Render Free Tier Spin-Down (Cold Starts)
- **Behavior**: Free instances on Render spin down after 15 minutes of inactivity. When a new request arrives, it may take 20–40 seconds to spin back up.
- **How CareerCompass AI handles it**:
  - The frontend `Navbar.jsx` checks `/` health on initial load.
  - If the server is waking up, the status shows "Connecting...".
  - If a user submits a form during spin-up, `Dashboard.jsx` includes a built-in **Retry Evaluation** button so students never get stuck.

### 2. SQLite Database Persistence on Render
- On Render's Free tier, the local filesystem is ephemeral (resets on redeploy or container restart).
- For a college demonstration/portfolio, this is standard and functional.
- If persistent storage across deployments is desired in the future:
  - Add a **Render Persistent Disk** mounted at `/data` and set `DB_PATH=/data/career_system.db`.
  - Or connect a free PostgreSQL database on Render (`render.com/docs/databases`).
