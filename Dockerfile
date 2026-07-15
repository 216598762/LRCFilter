# Multi-stage build for lrcfilter
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /install /usr/local

# Create non-root user
RUN useradd -m -u 1000 lrcfilter
USER lrcfilter
WORKDIR /home/lrcfilter

# Copy application code (after dependencies are installed for better caching)
COPY --chown=lrcfilter:lrcfilter . .

# Install the package
RUN pip install --no-cache-dir -e .

# Default entrypoint
ENTRYPOINT ["python", "-m", "lrcfilter"]
CMD ["--help"]
