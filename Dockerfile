FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for some packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (needed for tiktoken)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --prefer-binary -r requirements.txt

# Copy the rest of the project
COPY . .

# Set environment variables
ENV PYTHONPATH=src
ENV CREWAI_TELEMETRY_OPT_OUT=true

# Create outputs directory
RUN mkdir -p outputs

# Expose port
EXPOSE 8000

# Start the FastAPI server
CMD uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}
