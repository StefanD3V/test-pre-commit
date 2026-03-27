# Aviana Backend

Backend application for Aviana, a smart airport workforce platform that helps supervisors monitor staff deployment in real time, respond to disruptions, and improve operational performance.

This project is built with Django, Django REST Framework, and Celery, and is structured from the beginning with a scalable architecture suitable for multi-airport deployment.

## Tech Stack

### Core
- **Django** — web framework
- **Django REST Framework** — API layer
- **Python 3.12** — runtime

### Data Stores
- **PostgreSQL + PostGIS** — relational database with geospatial support (zones, geofences)
- **Redis** — Celery broker, caching, real-time worker positions
- **BigQuery** — data warehouse for GPS telemetry, analytics, and ML training data

### Task Processing
- **Celery** — distributed task queue for background and real-time processing
- **Celery Beat** — periodic task scheduling

### Authentication
- **Custom User model** — extending Django's `AbstractUser` for future flexibility

### Code Quality
- **Ruff** — linting and formatting
- **Django test framework** — testing

## Current Project Goal

At this stage, the project is in its initial backend setup phase.

The main goal right now is to establish:

- a clean and scalable project structure
- base Django configuration with environment-based settings
- PostgreSQL + PostGIS database setup
- custom user model (before first migration)
- CI pipeline with linting and testing
- readiness for future Celery, Redis, and BigQuery integration

This means the project is being prepared to support:

- typed API endpoints
- GPS coordinate ingestion and storage
- real-time worker position tracking
- background analysis and insight detection
- AI-driven workforce plan optimization
- multi-airport multi-tenant architecture

## Project Structure

```
aviana-backend/
  config/
    __init__.py
    settings.py
    urls.py
    asgi.py
    wsgi.py

  aviana/
    __init__.py
    admin.py
    apps.py
    models.py
    views.py
    urls.py
    serializers.py
    tests/
      __init__.py
      test_models.py
      test_views.py

  .env
  .env.example
  .gitignore
  docker-compose.yml
  manage.py
  requirements.txt
  ruff.toml
```

## Structure Explanation

### config/
Django project configuration. Settings, root URL config, WSGI/ASGI entry points.

Environment-specific values (secrets, database credentials, feature flags) are loaded from `.env` via `django-environ`.

### aviana/
Single application module containing all business logic.

- **models.py** — all domain models (airports, workers, zones, tracking, flights)
- **views.py** — API views and viewsets
- **serializers.py** — DRF serializers for request/response handling
- **urls.py** — app-level URL routing
- **tests/** — test modules organized by concern

As the project grows, this can be split into separate Django apps if needed, but starting with a single app keeps things simple and avoids premature abstraction.

### docker-compose.yml
Local development services:

- **PostgreSQL + PostGIS** — database
- **Redis** — broker and cache

BigQuery is accessed directly via the `aviana_dev` dataset in GCP — no local emulation needed.

## Architecture Principles

This project is being organized with the following principles in mind:

- **multi-tenant from day one** — airports are a data dimension, not separate deployments
- **separation of data stores by workload** — Postgres for operational data, Redis for real-time state, BigQuery for high-volume telemetry
- **managed services in production** — Cloud SQL, Memorystore, BigQuery (no self-hosted databases in K8s)
- **infrastructure as code** — Terraform for cloud resources, Helm for K8s deployments
- **stateless application layer** — all app services run on GKE Autopilot, databases are fully managed

## Data Flow

### GPS coordinate ingestion
Badges → LoRaWAN → ThingPark → ingestion endpoint → Redis (current position) + BigQuery (history)

### Background analysis
Celery Beat triggers → background workers query BigQuery for patterns + Postgres/PostGIS for zone geometries → write insights/alerts to Redis

### AI optimization
Celery Beat triggers → AI worker reads from Redis + Postgres + BigQuery → runs optimization model → writes updated plan to Postgres

### Dashboard
Frontend polls Django API → API reads current positions and alerts from Redis, plans and schedules from Postgres → serves to live dashboard

## Environment Setup

### Prerequisites
- Python 3.12
- Docker and Docker Compose

### Local Development

```bash
# Start database services
docker compose up -d

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Environment Variables

See `.env.example` for all required variables:

```
SECRET_KEY=
DEBUG=True
DB_NAME=aviana
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## Scripts

Common commands used in the project:

```bash
python manage.py runserver        # start dev server
python manage.py test             # run tests
python manage.py shell_plus       # interactive shell with auto-imports
python manage.py makemigrations   # create new migrations
python manage.py migrate          # apply migrations
ruff check .                      # lint
ruff check --fix .                # lint and auto-fix
ruff format .                     # format code
ruff format --check .             # check formatting
```