# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`keyvault` is a Python package (published on PyPI) for reading, creating, and deleting secrets in Azure Key Vault. It also supports loading secrets from local `.env` files and setting them as environment variables.

## Development Commands

```bash
# Install dependencies (runtime + dev)
uv sync --dev

# Linting
uv run ruff check .

# Formatting
uv run ruff format .

# Check formatting without modifying
uv run ruff format --check .

# Tests (require Azure credentials and TEST_KEYVAULT_NAME env var)
uv run pytest keyvault

# Build
uv build
```

Tests are integration tests that hit a real Azure Key Vault. They require these environment variables: `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`, `TEST_KEYVAULT_NAME`. Locally, these can be set via a `.env` file (loaded by `python-dotenv` in `keyvault/tests/__init__.py`).

## Architecture

The package has three source modules under `keyvault/`:

- **`auth.py`** — Creates an authenticated `SecretClient` using `DefaultAzureCredential` and a keyvault name. All other modules use `create_keyvault_client()` from here.
- **`get_secrets.py`** — Reading secrets: `get_keyvault_secrets()` returns a dict of all enabled secrets, `secrets_to_environment()` sets them as env vars (replacing `-` with `_` in names).
- **`utils.py`** — Writing/deleting secrets: `dict_to_keyvault()`, `dotenv_to_keyvault()`, `delete_keyvault_secrets()`, and the local-only `get_dotenv_secrets()`.

Public API is re-exported from `keyvault/__init__.py`.

## Code Style

- Ruff for both linting and formatting (line-length=100)
- Lint rules: E, F, I (isort), W with max-complexity=10
- Pre-commit hooks enforce formatting on commit

## Package Config

- Build: setuptools (configured in `pyproject.toml`)
- Version is in `pyproject.toml` under `[project]`
- Dependencies managed with uv (`uv sync --dev`)
- Published to PyPI on GitHub release via `.github/workflows/pypi.yml`
