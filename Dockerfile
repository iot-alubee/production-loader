# Cloud Functions (2nd gen) / Cloud Run — HTTP handler from main.py
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD exec functions-framework --target=get_google_sheet_data --port="${PORT}" --signature-type=http
