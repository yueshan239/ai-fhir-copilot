FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./

# Install CPU-only torch first (~30MB vs ~2GB with CUDA)
RUN uv pip install --system --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install remaining dependencies (torch already present, skipped)
RUN uv pip install --system --no-cache-dir -r pyproject.toml

# Pre-download MiniLM model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# Copy application code
COPY . .

# Create vectorstore directory
RUN mkdir -p vectorstore

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
