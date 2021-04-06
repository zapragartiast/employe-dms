#!/usr/bin/sh

ENV_FILE=.env
DBNAME=empdb
DBNAME_TEST=empdb_test
PGPASS=mypostgre_password

export PG_PASSWORD="$PGPASS"

if [ ! -f $ENV_FILE ]; then
  echo "File $ENV_FILE not found!"
  echo "Create $ENV_FILE file"
  touch $ENV_FILE
  cat <<-EOF > $ENV_FILE
    # database environment variable
    DATABASE_USER=postgres
    DATABASE_PASS=mypostgre_password
    DATABASE_HOST=127.0.0.1
    DATABASE_NAME=$DBNAME

    # JWT environment variable
    SECRET_KEY=super-secret-and-private
    PROD_SECRET_KEY=541e984103d4099bb8383050c56d511e733d85e6ab889a1c363ced6517
EOF
  echo "The $ENV_FILE has been created."
else
  echo "The $ENV_FILE found. Continue process."
fi

cat << EOF | psql postgresql://postgres:$PG_PASSWORD@127.0.0.1:5432

BEGIN;
SELECT version();
END;
CREATE DATABASE $DBNAME;
CREATE DATABASE $DBNAME_TEST;

EOF

unset PG_PASSWORD