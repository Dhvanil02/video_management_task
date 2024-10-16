#!/usr/bin/env bash

# Usage: wait-for-it.sh host:port [-- timeout] [-- command args]
# This script will wait for a service to be available.

host="$1"
shift
timeout=15

# Wait for the host to become available
for i in $(seq 1 $timeout); do
  nc -z "$host" && break
  echo "Waiting for $host..."
  sleep 1
done

# Execute the command if provided
if [ "$#" -gt 0 ]; then
  exec "$@"
fi
