FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

WORKDIR /app

# Install base build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies from requirements file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY backend /app/backend/
COPY ml /app/ml/
COPY data /app/data/

# Run the training script to bake the ML artifacts into the container image
WORKDIR /app/ml
RUN python trainer.py

# Switch to the backend directory and expose the target port
WORKDIR /app/backend
EXPOSE 8000

# Use uvicorn as the ASGI server
# The --host 0.0.0.0 and --port $PORT are required for cloud routing
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
