#!/usr/bin/env bash
function call_psql {
    psql "$POSTGRES_DB" $1 $2 $3 --username "$POSTGRES_USER"
}

cat /sql/install.versioning.sql | call_psql --quiet

# schema version 000:
cat /sql/000/extensions.sql | call_psql -a -v ON_ERROR_STOP=1
cat /sql/000/symbols.sql | call_psql -a -v ON_ERROR_STOP=1
