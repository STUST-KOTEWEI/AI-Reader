# Project HOLO - Docker Configuration
# Multi-stage build for optimized production image

# ============================================================
# Backend Build Stage
# ============================================================
FROM python:3.11-slim as backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy application code
COPY holo/ ./holo/
COPY web/backend/ ./web/backend/
COPY tests/ ./tests/

# Expose backend port
EXPOSE 8000

# Run the backend server
CMD ["uvicorn", "web.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]


# ============================================================
# Frontend Build Stage
# ============================================================
FROM node:20-alpine as frontend-builder

WORKDIR /app

# Copy package files
COPY web/frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY web/frontend/ ./

# Build frontend
RUN npm run build


# ============================================================
# Production Stage
# ============================================================
FROM python:3.11-slim as production

WORKDIR /app

# Install nginx and system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from backend stage
COPY --from=backend /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend /usr/local/bin /usr/local/bin

# Copy application code
COPY holo/ ./holo/
COPY web/backend/ ./web/backend/

# Copy built frontend from frontend-builder stage
COPY --from=frontend-builder /app/dist /var/www/html

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Expose ports
EXPOSE 80 8000

# Start both nginx and uvicorn
CMD nginx && uvicorn web.backend.main:app --host 0.0.0.0 --port 8000
