FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD if [ "$MODE" = "background" ]; then \
      echo "Starting background worker..." && \
      python -m app.background_main; \
    else \
      echo "Starting FastAPI server..." && \
      uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --use-colors; \
    fi

