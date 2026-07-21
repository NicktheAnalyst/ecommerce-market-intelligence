FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client drivers and build utilities
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Entrypoint: automatically seeds DB, executes pipeline, and launches Streamlit
CMD ["sh", "-c", "python -m database.seed && python run_pipeline.py && streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]