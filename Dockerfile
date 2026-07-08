FROM python:3.11-slim

WORKDIR /app/backend

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY ai_engine/ /app/ai_engine/

# Both backend (for api.*, main) and /app (for ai_engine.*) must be resolvable
ENV PYTHONPATH=/app/backend:/app

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
