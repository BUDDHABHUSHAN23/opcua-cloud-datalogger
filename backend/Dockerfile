# FROM python:3.11-slim-bookworm

# WORKDIR /app

# # Copy everything from the current context into /app
# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Use slim Python image
FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Install OS-level dependencies (for psycopg2, reportlab, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Add test tools directly into requirements
RUN echo "\n# Test dependencies" >> requirements.txt && \
    echo "pytest" >> requirements.txt && \
    echo "pytest-asyncio" >> requirements.txt && \
    echo "httpx" >> requirements.txt

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Default CMD (can be overridden with docker exec for testing)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
