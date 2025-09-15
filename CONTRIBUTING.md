# Contributing to the NLQ Platform

First off, thank you for considering contributing! Your help is greatly appreciated.

This document provides guidelines for contributing to the project. Please feel free to propose changes to this document in a pull request.

## How to Contribute

We use the standard GitHub flow for contributions:

1.  **Fork the repository** to your own GitHub account.
2.  **Clone your fork** to your local machine.
3.  **Create a new branch** for your changes: `git checkout -b my-feature-branch`.
4.  **Make your changes** and commit them with clear, descriptive messages.
5.  **Push your branch** to your fork on GitHub.
6.  **Open a pull request** from your branch to the `main` branch of the original repository.

## Development Setup

To get your local development environment set up, please follow the instructions in the main [README.md](./README.md) file. The recommended setup uses Docker Compose to simplify dependency management.

## Running Tests

A comprehensive test suite is crucial for maintaining code quality and stability. Before submitting a pull request, please ensure that all existing tests pass and that you have added new tests for any new functionality.

To run the backend tests, execute the following command:

```sh
# Ensure the containers are running
docker compose exec api pytest
```

(Note: This command assumes the backend service is named `api` in `docker-compose.yml` and that `pytest` is the testing framework.)

## Code Style

Please try to match the existing code style. We follow standard conventions for Python (PEP 8) and JavaScript/TypeScript.

For the backend, we use `black` for code formatting and `ruff` for linting. You can run these tools locally before committing your changes.

```sh
# Example commands (to be run inside the backend container)
docker compose exec api black .
docker compose exec api ruff .
```

## Submitting a Pull Request

-   Provide a clear title and description for your pull request.
-   Reference any related issues (e.g., "Closes #123").
-   Ensure all tests are passing in the CI pipeline.
-   Be prepared to address feedback and make changes to your submission.

Thank you for your contribution!
