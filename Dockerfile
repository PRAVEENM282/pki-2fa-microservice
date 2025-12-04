FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app
# Install cron
RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*
# Copy deps
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
# Copy code
COPY . .
# Setup cron
COPY cron/2fa-cron /etc/cron.d/2fa-cron
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron
# Permissions
RUN mkdir -p /data /cron && chmod 755 /data /cron

EXPOSE 8080
CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8080