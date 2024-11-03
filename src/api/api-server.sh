#!/bin/bash

COMMAND=$1
SERVER_PID_PATH=/tmp/server.pid

if [ -z "$2" ]; then
  SERVER_PATH="src.asgi:app"
elif [ "$2" == 'mock' ]; then
  SERVER_PATH="mock:app"
else
  echo "Unknown mode running" && exit 1
fi

if [ "$COMMAND" == 'start' ]; then
  echo "Starting $MODE server"
  uvicorn "$SERVER_PATH" --log-config uvicorn-log.ini &
  echo $! > $SERVER_PID_PATH
  exit 0
fi

if [ "$COMMAND" == 'stop' ]; then
  echo "Stopping $MODE server"
  kill "$(cat $SERVER_PID_PATH)"
  exit 0
fi

echo "Unknown command $COMMAND"
exit 1