# Usa uma imagem base oficial do Python 3.12 slim para menor tamanho
FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos para o contêiner
COPY requirements.txt .

# Instala as dependências do sistema e do projeto
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto para o contêiner
COPY . .

# Exponha a porta que o FastAPI usará (8000)
EXPOSE 8000

# Configura o comando para rodar a aplicação
CMD if [ "$MODE" = "background" ]; then \
      echo "Starting background worker..." && \
      python -m app.background_main; \
    else \
      echo "Starting FastAPI server..." && \
      uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --use-colors; \
    fi

