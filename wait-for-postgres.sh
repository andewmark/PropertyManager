#!/bin/sh
set -e

host="$1"
shift
cmd="$@"

: "${POSTGRES_USER:=dev}"
: "${POSTGRES_PASSWORD:=dev}"
: "${POSTGRES_DB:=test_db}"

echo "Waiting for Postgres at $host..."

# Wait until Postgres is ready
until PGPASSWORD=$POSTGRES_PASSWORD pg_isready -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  sleep 2
done

echo "Postgres is ready!"
exec $cmd
