# 🛒 FastAPI E-commerce API Base

## 🇧🇷 Descrição

Este projeto é uma **base para APIs de e-commerce** desenvolvida com **FastAPI**, projetada para ser modular, escalável e fácil de expandir.  
Inclui autenticação com **JWT**, integração com **PostgreSQL**, ORM via **SQLAlchemy**, versionamento de rotas e estrutura de pastas organizada para crescimento de aplicações reais.

Ideal para iniciar rapidamente projetos de backend modernos com padrões profissionais.

---

## 🚀 Tecnologias Utilizadas

- **FastAPI** — Framework web moderno e performático  
- **SQLAlchemy** — ORM para manipulação de banco de dados  
- **PostgreSQL** — Banco de dados relacional  
- **Alembic** — Migrações de banco  
- **Python-Jose + Passlib** — Autenticação JWT e hash de senhas  
- **Docker + Docker Compose** — Containerização e ambiente isolado  
- **Pydantic** — Validação de dados  
- **FastAPI-Mail** — Envio de e-mails com templates Jinja2
- **Pytest** — Testes unitários

---

## ⚙️ Estrutura de Pastas

```
app/
├── controller/        # Rotas e controladores
│   └── user/
├── core/              # Configurações centrais e autenticação
├── models/             # Modelos SQLAlchemy
├── db/                # Camada de acesso ao banco
├── migrations/        # Migraçoes do db
├── schemas/           # Schemas (Pydantic)
├── services/          # Lógica de negócio
├── templates/         # Templates HTML
├── dependencies/      # Utilitários (e-mail, segurança, etc.)
└── main.py            # Ponto de entrada da aplicação
```

---

## 🧰 Como Executar o Projeto

### 🔹 Opção 1 — Execução Local

Pré-requisitos:
- Python 3.12+
- PostgreSQL ativo e configurado no `.env`

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload
```

A API estará disponível em:
> http://127.0.0.1:8000

---

### 🔹 Opção 2 — Com Docker

```bash
sudo docker compose up --build
```

A API será iniciada automaticamente.  
Por padrão:  
> http://localhost:8000

---

## 🔐 Autenticação e Rotas Básicas

### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded
```
**Body:**
```
username=admin@test.com
password=qazwsx
```

### Registro
```http
POST /users/register
```
**JSON Body:**
```json
{
  "name": "admin",
  "email": "admin@test.com",
  "password": "qazwsx"
}
```

### Health Check
```http
GET /health
```

Retorna `200 OK` se o servidor estiver online.

---

## 🧩 Futuras Implementações

- 🛍️ Módulo de produtos  
- 🛒 Carrinho de compras  
- 💳 Sistema de pagamentos  
- 📦 Controle de pedidos e estoque  
- 👤 Painel administrativo  

---

## 📄 Licença
Projeto livre para uso e modificação sob a licença **MIT**.

---

## 🇺🇸 English Version

# 🛒 FastAPI E-commerce API Base

## 🧠 Overview

This project serves as a **base template for e-commerce APIs** built with **FastAPI**, designed for scalability and modularity.  
It includes **JWT authentication**, **PostgreSQL** integration, and a clean architecture to speed up backend development.

---

## 🚀 Tech Stack

- **FastAPI** — Modern web framework  
- **SQLAlchemy** — ORM for database management  
- **PostgreSQL** — Relational database  
- **Alembic** — Database migrations  
- **Python-Jose + Passlib** — JWT authentication  
- **Docker + Docker Compose** — Containerized setup  
- **Pydantic** — Data validation  
- **FastAPI-Mail** — Email sending with Jinja2 templates
- **Pytest** — Unit tests

---

## ⚙️ Project Structure

```
app/
├── controller/        # Controllers and routes
│   └── user/
├── core/              # Config and authentication
├── models/            # SQLAlchemy models
├── db/                # Database access layer
├── migrations/        # Database migrations
├── schemas/           # Pydantic schemas (Pydantic)
├── services/          # Business logic
├── templates/         # HTML templates
├── dependencies/      # Utilitaries (e-mail, segurança, etc.)
└── main.py            # Application entry point
```

---

## 🧰 How to Run

### 🔹 Option 1 — Local Run

Requirements:
- Python 3.12+
- PostgreSQL running and configured in `.env`

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload
```

API available at:
> http://127.0.0.1:8000

---

### 🔹 Option 2 — Docker Run

```bash
sudo docker compose up --build
```

API available at:
> http://localhost:8000

---

## 🔐 Authentication & Routes

### Login
```http
POST /auth/login
```
**Form data:**
```
username=admin@test.com
password=qazwsx
```

### Register
```http
POST /users/register
```
**JSON:**
```json
{
  "name": "admin",
  "email": "admin@test.com",
  "password": "qazwsx"
}
```

### Health Check
```http
GET /health
```

Returns `200 OK` if the server is online.

---

## 🧩 Future Implementations

- 🛍️ Product module  
- 🛒 Shopping cart  
- 💳 Payment system  
- 📦 Orders and inventory  
- 👤 Admin dashboard  

---

## 📄 License
Free to use and modify under the **MIT License**.
