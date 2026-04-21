# HNG Stage 2 — Containerized Job Processing System

A multi-service job processing system containerized with Docker and deployed with a full CI/CD pipeline.

## Services

- **Frontend** (Node.js/Express) — Job submission dashboard on port 3000
- **API** (Python/FastAPI) — Job creation and status on port 8000
- **Worker** (Python) — Processes jobs from Redis queue
- **Redis** — Shared message queue

## Prerequisites

- Docker
- Docker Compose v2+
- Git

## Run Locally From Scratch

```bash
# Clone the repo
git clone https://github.com/Bobleeswagger09/hng14-stage2-devops.git
cd hng14-stage2-devops

# Create .env file
cp .env.example .env
# Edit .env and set your REDIS_PASSWORD

# Build and start all services
docker compose up --build

# Visit the dashboard
open http://localhost:3000
```

## Successful Startup Looks Like

✔ Container redis-1     Healthy
✔ Container api-1       Healthy
✔ Container worker-1    Started
✔ Container frontend-1  Started
Frontend running on port 3000

## Environment Variables

See `.env.example` for all required variables.

## Endpoints

- `GET /` — Job dashboard UI
- `POST /submit` — Submit a new job
- `GET /status/:id` — Get job status
