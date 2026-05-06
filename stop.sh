#!/bin/bash

echo "========================================"
echo " Stopping Messenger App by Ports"
echo "========================================"

PORTS=(8001 8002 8003 5173)

for PORT in "${PORTS[@]}"; do
  PID=$(lsof -ti tcp:$PORT || true)

  if [ -n "$PID" ]; then
    echo "Stopping process on port $PORT with PID $PID"
    kill $PID 2>/dev/null || true
  else
    echo "No process found on port $PORT"
  fi
done

echo ""
echo "=== PostgreSQL ==="
read -p "Do you want to stop PostgreSQL too? (y/n): " STOP_PG

if [ "$STOP_PG" = "y" ] || [ "$STOP_PG" = "Y" ]; then
  sudo service postgresql stop || true
  echo "PostgreSQL stopped."
else
  echo "PostgreSQL left running."
fi

echo ""
echo "Everything stopped."