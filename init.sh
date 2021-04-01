#!/usr/bin/sh

PGPASS=mypostgre_password
export PG_PASSWORD="$PGPASS"

cat << EOF | psql postgresql://postgres:$PG_PASSWORD@127.0.0.1:5432
BEGIN;

SELECT version();

END;
EOF

unset PG_PASSWORD