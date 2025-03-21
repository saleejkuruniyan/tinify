# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apt-get update \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement files and install dependencies into /install
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --prefix=/install mysqlclient \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.11-slim AS final

WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install runtime dependencies only (libmysqlclient)
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . /app

# Expose application port
EXPOSE 8000

# Run the application (customize if needed)
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
