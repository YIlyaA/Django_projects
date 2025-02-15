#!/bin/bash

# exit if a command exits with a non-zero status
set -o errexit

# exit if pipline failed
set -o pipfail

# exit if an uninitialized variable is used
set -o nounset

python << END

import system
import time
import psycopg2
suggest_unrecoverable_after = 30
start = time.time()
while True:
    try:
        psycopg2.connect(
            dbname="${POSTGRES_DB}",
            user="${POSTGRES_USER}",
            password="${POSTGRES_PASSWORD}",
            host="${POSTGRES_HOST}",
            port="${POSTGRES_PORT}",
        )
        break
    except psycopg2.OperationalError as error:
        sys.stderr.write("Waiting for PostgreSQL to become available ... \n")
        if time.time() - start >= suggest_unrecoverable_after:
            sys.stderr.write("This is taking longer than expexcted. The following exception 
            indicative of an unrecoverable error: '{}'\n".format(error))
            time.sleep(3)
END

echo >&2 'PostgreSQL is available'

exec "$@"