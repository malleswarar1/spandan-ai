FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8080

# Start command
CMD cd backend && uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
