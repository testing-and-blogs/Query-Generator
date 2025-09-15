# Monitoring & Observability

A robust monitoring and observability strategy is essential for maintaining the health, performance, and reliability of the NLQ platform, especially in a production environment. This document outlines the tools and practices we use.

## Guiding Principles

-   **Structured Logging**: All application components (Django, Celery workers) output logs in a structured format (e.g., JSON). This allows for easier parsing, filtering, and analysis in a centralized logging system.
-   **Request Correlation**: A unique request ID is generated for each incoming API request and propagated through all services (API, workers) and logs. This allows for tracing the entire lifecycle of a request.
-   **Health Checks**: A dedicated, unauthenticated endpoint (e.g., `/api/v1/health/`) is provided for basic health checks, suitable for use by load balancers and container orchestrators.

## Core Observability Components

The default deployment includes foundational observability features. An advanced, open-source monitoring stack can be enabled for deeper insights.

### 1. Structured Logs

Logs are the primary source of information for debugging. Key events are logged, including:
- API requests and responses
- User authentication events
- Tenant activity
- Celery task execution (enqueue, start, success, failure)
- Errors and exceptions with full stack traces

### 2. Basic Metrics

The application is instrumented to expose basic metrics, such as:
- API request latency, volume, and error rates.
- NL→SQL generation performance and token usage.
- Query execution counts and durations.

## Optional Observability Stack

For comprehensive monitoring, an optional stack based on popular open-source tools can be deployed alongside the main application.

### How to Enable

This stack is defined in the `docker-compose.yml` file under a separate profile named `observability`. You can enable it by running:

```sh
docker compose --profile observability up -d
```

This will launch the following additional services:

-   **Prometheus**: A time-series database that scrapes and stores metrics from the application and infrastructure.
-   **Grafana**: A visualization tool for creating dashboards from Prometheus data. Pre-built dashboards for Django, Celery, and system metrics can be included.
-   **Celery Flower**: A real-time web-based monitor for Celery. It provides visibility into task progress, worker status, and task history. It is accessible at `http://localhost:5555`.
-   **Langfuse (Optional)**: A self-hostable, open-source LLM engineering platform. If enabled, it can trace all interactions with the NL→SQL provider, including the exact prompts, responses, latency, and token counts. This is invaluable for debugging and improving prompt effectiveness.

### Accessing the Tools

When running the `observability` profile locally, the tools are typically available at:
-   **Grafana**: `http://localhost:3001`
-   **Prometheus**: `http://localhost:9090`
-   **Flower**: `http://localhost:5555`
-   **Langfuse**: `http://localhost:3002` (if configured)
