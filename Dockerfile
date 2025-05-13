# # FROM python:3.11.8-alpine

# # WORKDIR /apps

# # # Install build dependencies for Alpine
# # RUN apk add --no-cache \
# #     build-base \
# #     libffi-dev \
# #     musl-dev \
# #     gcc \
# #     postgresql-dev \
# #     python3-dev \
# #     libxml2-dev \
# #     libxslt-dev \
# #     jpeg-dev \
# #     zlib-dev \
# #     openblas-dev \
# #     freetype-dev \
# #     bash \
# #     git

# # # Copy app and dependencies
# # COPY ./app ./app
# # COPY ./requirements.txt .
# # COPY ./bin/app.sh ./app.sh

# # # Install Python packages
# # RUN pip install --no-cache-dir --upgrade pip \
# #  && pip install --no-cache-dir -r requirements.txt

# # # Make the shell script executable
# # RUN chmod +x ./app.sh

# # # Expose the port used by Gunicorn
# # EXPOSE 8080

# # # Run your shell script
# # ENTRYPOINT ["./app.sh"]

# FROM python:3.11.8-alpine

# WORKDIR /apps

# # Install build dependencies
# RUN apk add --no-cache \
#     build-base \
#     libffi-dev \
#     musl-dev \
#     gcc \
#     postgresql-dev \
#     python3-dev \
#     libxml2-dev \
#     libxslt-dev \
#     jpeg-dev \
#     zlib-dev \
#     openblas-dev \
#     freetype-dev \
#     bash \
#     git \
#     cargo \
#     libressl-dev

# # Set environment variables to avoid Python buffering and ensure logs show
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Copy files
# COPY ./app ./app
# COPY ./requirements.txt .
# COPY ./bin/app.sh ./app.sh

# # Upgrade pip & install requirements
# RUN pip install --upgrade pip \
#  && pip install --no-cache-dir -r requirements.txt

# # Make the shell script executable
# RUN chmod +x ./app.sh

# # Expose port for the app
# EXPOSE 8080

# ENTRYPOINT ["./app.sh"]

# Use Python slim base image
FROM python:3.11-slim

# Set working directory
WORKDIR /apps

# Install system dependencies (curl, ping, and Ollama)
RUN apt-get update && apt-get install -y curl iputils-ping && \
    curl -fsSL https://ollama.ai/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app ./app
COPY ./bin/app.sh ./app.sh
COPY ./.env ./.env

# Copy pretrained model (optional, comment out if mounting as a volume)
# COPY ./models/bge-m3 ./models/bge-m3
# # Copy pretrained models
# COPY ./models/bge-m3 ./models/bge-m3
# COPY ./models/bge-reranker-large ./models/bge-reranker-large

# Ensure scripts are executable
RUN chmod +x app.sh

# Create non-root user
RUN useradd -m appuser && chown -R appuser /apps
USER appuser

# Expose port
EXPOSE 8080

# Run the entrypoint script
ENTRYPOINT ["./app.sh"]