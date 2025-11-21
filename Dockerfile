FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libpq-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

EXPOSE 8000

CMD if [ "$MODE" = "background" ]; then \
      echo "Starting background worker..." && \
      python -m app.background_main; \
    else \
      echo "Starting FastAPI server..." && \
      uvicorn app.main:app --host 0.0.0.0 --port 8000; \
    fi
