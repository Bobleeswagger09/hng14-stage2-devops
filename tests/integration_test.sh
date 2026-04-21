#!/bin/bash
set -e

echo "Starting integration test..."

# Wait for frontend to be ready
MAX_WAIT=60
WAITED=0
until curl -sf http://localhost:3000 > /dev/null; do
    if [ $WAITED -ge $MAX_WAIT ]; then
        echo "Timeout waiting for frontend"
        exit 1
    fi
    sleep 2
    WAITED=$((WAITED + 2))
done

echo "Frontend is up. Submitting job..."

# Submit a job
RESPONSE=$(curl -sf -X POST http://localhost:3000/submit)
JOB_ID=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job submitted: $JOB_ID"

# Poll until completed
MAX_WAIT=60
WAITED=0
while true; do
    STATUS=$(curl -sf http://localhost:3000/status/$JOB_ID | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
    echo "Status: $STATUS"
    if [ "$STATUS" = "completed" ]; then
        echo "Job completed successfully!"
        exit 0
    fi
    if [ $WAITED -ge $MAX_WAIT ]; then
        echo "Timeout waiting for job to complete"
        exit 1
    fi
    sleep 2
    WAITED=$((WAITED + 2))
done
