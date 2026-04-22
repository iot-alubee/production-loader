# Cloud Functions (2nd gen) / Cloud Run: Python HTTP function
# Build: docker build -t REGION-docker.pkg.dev/PROJECT/REPO/production-loader:latest .
# Push and deploy via Artifact Registry + gcloud functions deploy --docker-image=...

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8080

# Target must match the HTTP function name in main.py
CMD exec functions-framework --target=publish_iot --port="${PORT}" --signature-type=http
