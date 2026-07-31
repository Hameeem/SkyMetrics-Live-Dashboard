# SkyMetrics Cloud & Local Deployment Guide

SkyMetrics is architected for flexible deployment across local Docker environments, cloud app platforms (Render, Railway), managed database services (Neon, Supabase), and independent dashboard hosting (Streamlit Community Cloud).

---

## 1. Local Deployment via Docker Compose

### Prerequisites
- Docker Engine & Docker Compose installed.

### Steps
```bash
# Clone repository
git clone https://github.com/your-username/SkyMetrics.git
cd SkyMetrics

# Build and launch multi-container stack
docker-compose up --build -d

# Verify running services
docker-compose ps
```

### Active Endpoints
- **Streamlit Dashboard**: `http://localhost` (via Nginx) or `http://localhost:8501`
- **FastAPI Backend API**: `http://localhost/api/` or `http://localhost:8000`
- **Swagger Documentation**: `http://localhost/docs`

---

## 2. Independent Streamlit Community Cloud Deployment

The Streamlit dashboard can be deployed standalone without embedding the backend code directly.

### Steps
1. Push the `SkyMetrics` repository to GitHub.
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New App**, select your GitHub repository and branch.
4. Set **Main file path** to `dashboard/app.py`.
5. Under **Advanced Settings > Secrets**, configure:
   ```toml
   BACKEND_API_URL = "https://your-skymetrics-backend.onrender.com"
   ```
6. Click **Deploy**. The app will automatically connect to your production API or run gracefully with local fallback datasets.

---

## 3. Backend Deployment on Render / Railway

### Render Setup
1. Create a **Web Service** on Render connected to your repository.
2. Select **Docker** environment and set Dockerfile path to `Dockerfile.backend`.
3. Add Environment Variables:
   - `DATABASE_URL`: Your PostgreSQL connection string (Neon or Supabase).
   - `SECRET_KEY`: Long random production key.
4. Deploy service and copy the public service URL for `BACKEND_API_URL`.

---

## 4. Database Setup (Neon / Supabase PostgreSQL)

1. Create a PostgreSQL instance on [Neon.tech](https://neon.tech/) or [Supabase](https://supabase.com/).
2. Copy the PostgreSQL connection string.
3. Update `DATABASE_URL` in your `.env` or Render environment settings.
4. Run migrations:
   ```bash
   alembic upgrade head
   python database/seed_data.py
   ```
