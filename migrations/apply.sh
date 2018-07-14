#!/usr/bin/env bash
function call_psql {
    export PGPASSWORD="$POSTGRES_PASSWORD";
    psql --host="$POSTGRES_HOST" --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" $1 $2 $3
}

mydir=$(dirname "$0")

cat "$mydir/install.versioning.sql" | call_psql --quiet

# schema version 000:
cat "$mydir/000/extensions.sql" | call_psql -a -v ON_ERROR_STOP=1
cat "$mydir/000/ticker.sql" | call_psql -a -v ON_ERROR_STOP=1
cat "$mydir/000/historical_price.sql" | call_psql -a -v ON_ERROR_STOP=1
