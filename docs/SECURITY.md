# Security Guidelines

This document outlines the security architecture, principles, and best practices for the NLQ platform. The system is designed with a security-first mindset, especially concerning multi-tenancy and access to external databases.

## Core Security Principles

### 1. Tenant Isolation

This is the most critical security guarantee of the platform.

-   **Database Layer**: All tenant-scoped data is strictly partitioned via a non-nullable `tenant_id` foreign key. Database constraints prevent cross-tenant data relations.
-   **API Layer**: A middleware component inspects every incoming request to identify the tenant based on the user's session. It attaches the `tenant` object to the request.
-   **ORM Layer**: A custom Django Manager/QuerySet (`TenantQuerySet`) is used for all tenant-scoped models. It automatically applies a `WHERE tenant_id = ?` filter to every database query, making it impossible for application code to accidentally access another tenant's data.
-   **Testing**: A dedicated test suite continuously verifies that users from one tenant cannot read, modify, or even detect the existence of resources belonging to another tenant.

### 2. Read-Only Execution Sandbox

To prevent malicious or accidental modification of user databases, all query execution is treated as hostile and sandboxed.

-   **Static Analysis**: Generated SQL is parsed using `sqlglot` before execution. The Abstract Syntax Tree (AST) is inspected to ensure it is a single `SELECT` statement. All other statement types (e.g., `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`) are rejected.
-   **Keyword Deny-List**: A list of forbidden keywords and functions (e.g., `xp_cmdshell`, `COPY`) provides an additional layer of defense.
-   **Resource Limits**: Queries are executed by a Celery worker with strict, configurable limits on execution time (`timeout`) and result set size (`max_rows` / `max_bytes`).
-   **Connection Permissions**: Database connections should be configured with read-only credentials whenever possible as a best practice.

### 3. Secrets Management

-   **Encryption at Rest**: All sensitive credentials, such as connection strings and passwords for source databases, are encrypted at rest in the application database using AES-256-GCM.
-   **Encryption Keys**: The encryption key is provided to the application via an environment variable (`DJANGO_SECRET_KEY` or a dedicated `ENCRYPTION_KEY`) and is never stored in the database. This allows for key rotation.
-   **Secrets in UI**: Secrets are always masked in the user interface and in logs.
-   **Environment Variables**: All sensitive configuration (API keys, database URLs) is managed via environment variables, not hardcoded in the source code. See `.env.example` for details.

## Specific Security Measures

-   **Authentication**: User passwords are hashed using a strong, modern algorithm (Argon2).
-   **Transport Security**: All external traffic is terminated by an Nginx reverse proxy that enforces TLS 1.2+.
-   **CSRF Protection**: Django's built-in Cross-Site Request Forgery protection is enabled for all session-based interactions.
-   **PII Awareness**: The system includes a mechanism to detect and warn users about columns that may contain Personally Identifiable Information (PII) based on name patterns. PII data from user queries is never logged.
-   **Dependency Management**: Dependencies are regularly scanned for known vulnerabilities using tools like `pip-audit` or GitHub's Dependabot.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it to us privately. Do not disclose it publicly until we have had a chance to address it. Please email a detailed report to `security@example.com` (replace with a real contact address). We appreciate your efforts to keep our platform secure.
