#!/usr/bin/sh

# This resource just for CI/CD test environments

ENV_FILE=.env

if [ ! -f $ENV_FILE ]; then
  echo "File $ENV_FILE not found!"
  echo "Create $ENV_FILE file"
  touch $ENV_FILE
  cat <<-EOF > .env
DATABASE_USER=postgres
DATABASE_PASS=mypostgre_password
DATABASE_HOST=127.0.0.1
DATABASE_NAME=emsdb
DATABASE_TEST=emsdb_test

SECRET_KEY=super-secret-and-private
PROD_SECRET_KEY=541e984103d4099bb8383050c56d511e733d85e6ab889a1c363ced6517
JWT_TTL=31556952
EOF
  echo "The $ENV_FILE has been created."
else
  echo "The $ENV_FILE found. Continue process."
fi

export $(xargs <$ENV_FILE)

export $DATABASE_PASS

cat << EOF | psql postgresql://$DATABASE_USER:$DATABASE_PASS@$DATABASE_HOST:5432
BEGIN;
SELECT version();
END;
CREATE DATABASE $DATABASE_NAME;
CREATE DATABASE $DATABASE_TEST;
EOF

unset $DATABASE_PASS

exit 0