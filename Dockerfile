# Use a stable Python image (not 3.14.4)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libzlib1g-dev \
        libjpeg-dev \
        libpng-dev \
        && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose port 8501 (Streamlit default)
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
