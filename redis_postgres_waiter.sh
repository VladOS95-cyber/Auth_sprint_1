#!/bin/sh

if [ "$REDIS_DB" = "redis" ]
then
    echo "Waiting for Redis db..."

    while ! nc -z $REDIS_HOST $REDIS_PORT; do
      sleep 0.1
    done

    echo "Redis db started"
fi

if [ "$POSTGRES_NAME" = "auth_database" ]
then
    echo "Waiting for Postgres db..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "Postgres db started"
fi

exec "$@"
