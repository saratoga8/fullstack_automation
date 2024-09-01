#!/bin/bash

COMMAND=$1
SERVER_PID_PATH=/tmp/server.pid

if [ "$COMMAND" == 'start' ]; then
  echo "Starting API server"
  uvicorn src.asgi:app --log-config uvicorn-log.ini &
  echo $! > $SERVER_PID_PATH
  exit 0
fi

if [ "$COMMAND" == 'stop' ]; then
  echo "Stopping API server"
  kill "$(cat $SERVER_PID_PATH)"
  exit 0
fi

echo "Unknown command $COMMAND"
exit 1