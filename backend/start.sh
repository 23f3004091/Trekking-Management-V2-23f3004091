#!/bin/bash

# 1. Define a cleanup function to kill all background processes on exit
cleanup() {
    echo ""
    echo "Shutting down all services..."
    # kill $(jobs -p) kills all processes started by this script
    kill $(jobs -p) 2>/dev/null
    echo "Done."
    exit
}

# 2. Trap Ctrl+C (SIGINT) and run the cleanup function
trap cleanup SIGINT EXIT

# 3. Start the services in the background using '&'
# echo "Starting Redis (The Broker)..."
# docker run --rm -p 6379:6379 redis &


echo "Starting Flask (The API)..."
python3 app.py &

echo "Starting Celery Worker (The Muscle)..."
celery -A app.celery worker --loglevel=info &

echo "Starting Celery Beat (The Brain/Clock)..."
celery -A app.celery beat --loglevel=info &

echo ""
echo "===================================================="
echo "All services are running! Press Ctrl+C to stop them."
echo "===================================================="

# 4. Wait keeps the script running until you explicitly kill it
wait