# Atlas Order Services

Atlas Order Services is a Python service for managing customer orders, product records, customer documents, partner event delivery, and operational audit records. It uses SQLite for local development and accepts a PostgreSQL SQLAlchemy URL through configuration.

> This synthetic application contains intentional and context-dependent security conditions for analysis It must not be deployed publicly or operationally.

## Setup

Python 3.14 is required.

```powershell
uv python install 3.14
uv sync --python 3.14 --group dev
```

To use PostgreSQL, set `ATLAS_DATABASE_URL` to a normal SQLAlchemy PostgreSQL URL before running the commands below. No application code changes are required.

## Database and sample records

```powershell
uv run alembic upgrade head
uv run python -m atlas_order_services.seed
```

The sample records use fictional organizations and identifiers. Re-running the seed command leaves an initialized database unchanged.

## Run the service

```powershell
uv run uvicorn atlas_order_services.main:app --host 127.0.0.1 --port 8080
```

Use `GET /health` to check process status and `GET /ready` to check persistence access. In deployed designs, network ownership of those probes belongs to the surrounding gateway.

## Authentication

Request a development token:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8080/api/v1/auth/token `
  -ContentType 'application/json' `
  -Body '{"username":"operator","password":"atlas-demo-password"}'
```

Call an API endpoint with the returned bearer token:

```powershell
$headers = @{ Authorization = 'Bearer atlas-demo-operator-token' }
Invoke-RestMethod http://127.0.0.1:8080/api/v1/customers -Headers $headers
```

The documented values are fictional local-development values only.

## Tests and checks

```powershell
uv run pytest
uv run ruff check .
uv run mypy src
uv run bandit -r src
uv run pip-audit
```

The test configuration requires at least 60% coverage. Some static-check output is expected from the supplied code and should be considered in its wider operating context.

## Containers

`docker compose up --build` starts the API container, applies the schema, and initializes local sample records. The compose configuration retains SQLite data and documents in named volumes. The image exposes port 8080; an external gateway is responsible for deployment-time routing and network policy.

## Local infrastructure example

`terraform/local-only` demonstrates a local-file output only. It does not contact an infrastructure provider or run automatically. If you choose to inspect it, use normal Terraform review and execution controls.

## Diff exercise

The `exercises` directory contains a feature request and two alternative patches that begin from this repository state. Start with the changed lines, expand into the relevant unchanged repository context, distinguish change-related conditions from unrelated existing conditions, and verify at least one correction before submitting your analysis.

Apply each alternative in a separate working copy:

```powershell
git apply exercises/candidate-a.patch
git apply exercises/candidate-b.patch
```

## Participant archive

Run the packaging script from PowerShell to create `atlas-order-services-participant.zip` at the repository root:

```powershell
./scripts/package-participant.ps1
```
