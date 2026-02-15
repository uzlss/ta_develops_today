# syntax=docker/dockerfile:1.4
# Development Dockerfile with multi-stage build and caching

# ============================================
# Stage 1: Builder - Install Python dependencies
# ============================================
FROM python:3.13-slim AS builder

WORKDIR /build

# Install build dependencies (only needed during pip install)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies to /opt/venv (accessible by all users)
# Using BuildKit cache mount for faster rebuilds
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt


# ============================================
# Stage 2: Runtime - Development image
# ============================================
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    PATH=/opt/venv/bin:$PATH

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-traditional \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy Python virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Don't copy the app code - it will be mounted as a volume
# Expose port for the FastAPI app
EXPOSE $PORT

# Command to run the FastAPI application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--proxy-headers", "--forwarded-allow-ips", "*"]
