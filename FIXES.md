# FIXES.md

## Bug 1 — api/main.py line 6
**Problem:** Redis host hardcoded to `localhost` — fails in Docker as services communicate by service name not localhost.
**Fix:** Changed to `os.getenv("REDIS_HOST", "redis")`

## Bug 2 — api/main.py line 6
**Problem:** Redis connection had no password authentication despite `.env` setting a password.
**Fix:** Added `password=os.getenv("REDIS_PASSWORD", "")` to Redis connection

## Bug 3 — api/main.py line 9
**Problem:** Queue name was `"job"` (singular) but worker was consuming from `"jobs"` (plural) — jobs would never be processed.
**Fix:** Changed `r.lpush("job", job_id)` to `r.lpush("jobs", job_id)`

## Bug 4 — api/main.py
**Problem:** Redis responses not decoded — `status.decode()` would fail since `decode_responses=True` was not set.
**Fix:** Added `decode_responses=True` to Redis connection, removed manual `.decode()` call

## Bug 5 — api/.env
**Problem:** Real credentials committed to the repository — major security vulnerability.
**Fix:** Removed file from git tracking with `git rm --cached api/.env`, added to `.gitignore`

## Bug 6 — worker/worker.py line 4
**Problem:** Redis host hardcoded to `localhost` — fails in Docker containers.
**Fix:** Changed to `os.getenv("REDIS_HOST", "redis")`

## Bug 7 — worker/worker.py line 4
**Problem:** Redis connection had no password authentication.
**Fix:** Added `password=os.getenv("REDIS_PASSWORD", "")` to Redis connection

## Bug 8 — worker/worker.py line 6
**Problem:** `import signal` present but never used — unnecessary import, bad practice.
**Fix:** Removed unused import

## Bug 9 — worker/worker.py
**Problem:** Queue name was `"job"` (singular) but API was pushing to `"jobs"` (plural).
**Fix:** Changed `r.brpop("job", timeout=5)` to `r.brpop("jobs", timeout=5)`

## Bug 10 — frontend/app.js line 5
**Problem:** `API_URL` hardcoded to `http://localhost:8000` — fails in Docker as frontend cannot reach API via localhost.
**Fix:** Changed to `process.env.API_URL || "http://api:8000"`

## Bug 11 — frontend/Dockerfile
**Problem:** `npm ci` requires `package-lock.json` which was not present in the repository.
**Fix:** Changed to `npm install --only=production`

## Bug 12 — api/requirements.txt
**Problem:** Missing `python-dotenv` needed to load environment variables from .env files.
**Fix:** Added `python-dotenv` to requirements.txt

## Bug 13 — worker/requirements.txt
**Problem:** Missing `python-dotenv` needed to load environment variables.
**Fix:** Added `python-dotenv` to requirements.txt
