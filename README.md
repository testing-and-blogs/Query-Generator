# SPEC-1: Schema-Aware NLQ Query Generator

This repository contains the source code for a multi-tenant, schema-aware, natural-language-to-SQL (NLQ) query generation platform. It allows users to connect to their databases, explore schemas visually, and generate SQL queries using natural language prompts.

## Overview

The platform is designed to be a secure, read-only query interface that supports major SQL databases. It provides a rich user experience with an auto-generated ERD, a schema browser, and a safe execution sandbox. The architecture is built for local development via Docker Compose and is ready for scalable production deployment.

## Tech Stack

- **Backend**: Python 3.13, Django 5.2, Django REST Framework, Celery, SQLAlchemy
- **Frontend**: React (Next.js/Vite), Tailwind CSS, React Flow
- **Application Database**: PostgreSQL 16+
- **Cache & Queue**: Redis 8+
- **Containerization**: Docker Compose, Nginx

## Key Features (MVP)

- **Multi-DB Support**: Connect to PostgreSQL, MySQL/MariaDB, SQLite, and MS SQL Server.
- **Schema Introspection**: Automatic discovery of tables, columns, relationships, and basic indexing.
- **Visual ERD**: Auto-layout Entity-Relationship Diagram with pan, zoom, and search.
- **NL-to-SQL**: Generate safe, read-only SQL queries from natural language prompts.
- **Sandboxed Execution**: Run queries with configurable timeouts and row limits.
- **Multi-Tenancy**: Secure tenant isolation at the database and API layers.
- **Admin & User Roles**: Superadmin, Tenant Admin, and Tenant User roles with scoped permissions.
- **Audit & History**: Track all queries and significant actions within a tenant.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Local Development

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Configure your environment:**
    - Copy the example environment file:
      ```sh
      cp .env.example .env
      ```
    - Review and update the variables in `.env` as needed. The default values are configured for the local Docker Compose setup.

3.  **Build and run the services:**
    ```sh
    docker compose up --build -d
    ```
    This will start all the required services, including the backend API, frontend server, database, and Redis.

4.  **Access the application:**
    - **API**: `http://localhost:8000/api/v1/`
    - **Frontend**: `http://localhost:3000`

## Project Structure

```
.
├── backend/         # Django backend source code
├── docs/            # Project documentation (Architecture, Security, etc.)
├── docker/          # Docker configurations (docker-compose.yml, Nginx)
├── frontend/        # React frontend source code
├── .env.example     # Example environment variables
└── README.md
```

For more detailed information, please refer to the documents in the `docs/` directory.
