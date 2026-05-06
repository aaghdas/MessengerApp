#!/bin/bash

set -e

AUTH_PID=""
USER_PID=""
MSG_PID=""
FRONTEND_PID=""

cleanup() {
  echo ""
  echo "========================================"
  echo " Stopping Messenger App Services"
  echo "========================================"

  if [ -n "$AUTH_PID" ]; then
    echo "Stopping Auth Service..."
    kill "$AUTH_PID" 2>/dev/null || true
  fi

  if [ -n "$USER_PID" ]; then
    echo "Stopping User Service..."
    kill "$USER_PID" 2>/dev/null || true
  fi

  if [ -n "$MSG_PID" ]; then
    echo "Stopping Messaging Service..."
    kill "$MSG_PID" 2>/dev/null || true
  fi

  if [ -n "$FRONTEND_PID" ]; then
    echo "Stopping Frontend..."
    kill "$FRONTEND_PID" 2>/dev/null || true
  fi

  echo ""
  echo "App services stopped."
  echo "PostgreSQL is still running."
  echo "To stop PostgreSQL:"
  echo "sudo service postgresql stop"
  echo ""

  exit 0
}

trap cleanup SIGINT SIGTERM

echo "========================================"
echo " Starting Messenger App"
echo "========================================"

echo ""
echo "=== Starting PostgreSQL ==="
sudo service postgresql start || true

echo ""
echo "=== Starting Auth Service on port 8001 ==="
cd auth_service
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001 &
AUTH_PID=$!
deactivate
cd ..

echo ""
echo "=== Starting User Service on port 8002 ==="
cd user_service
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8002 &
USER_PID=$!
deactivate
cd ..

echo ""
echo "=== Starting Messaging Service on port 8003 ==="
cd messaging_service
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8003 &
MSG_PID=$!
deactivate
cd ..

echo ""
echo "=== Starting React Frontend ==="
cd frontend
npm run dev -- --host 127.0.0.1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo " Messenger App is running"
echo "========================================"
echo ""
echo "Auth Service:"
echo "http://127.0.0.1:8001"
echo "http://127.0.0.1:8001/docs"
echo ""
echo "User Service:"
echo "http://127.0.0.1:8002"
echo "http://127.0.0.1:8002/docs"
echo ""
echo "Messaging Service:"
echo "http://127.0.0.1:8003"
echo "http://127.0.0.1:8003/docs"
echo ""
echo "Frontend:"
echo "http://127.0.0.1:5173"
echo ""
echo "To stop app services:"
echo "Press CTRL + C"
echo ""

wait