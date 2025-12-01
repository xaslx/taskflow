#!/usr/bin/env bash

set -e


until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.3
done


PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 \
  || PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB;"


alembic upgrade head

exec "$@"

