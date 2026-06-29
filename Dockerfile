FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/start.sh

ENV PYTHONPATH=/app/backend

ENTRYPOINT ["/bin/bash", "/app/start.sh"]
