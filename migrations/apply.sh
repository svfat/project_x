#!/usr/bin/env bash
function call_psql {
    export PGPASSWORD="$POSTGRES_PASSWORD";
    psql --host="$POSTGRES_HOST" --username="$POSTGRES_USER" --dbname="$POSTGRES_DB" $1 $2 $3
}

script_dir=$(dirname "$0")

cat "$script_dir/install.versioning.sql" | call_psql --quiet

# schema version 000:
cat "$script_dir/000/extensions.sql" | call_psql -a -v ON_ERROR_STOP=1
cat "$script_dir/000/ticker.sql" | call_psql -a -v ON_ERROR_STOP=1
cat "$script_dir/000/historical_price.sql" | call_psql -a -v ON_ERROR_STOP=1
cat "$script_dir/000/insider_trade.sql" | call_psql -a -v ON_ERROR_STOP=1
