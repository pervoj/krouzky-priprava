#!/bin/bash

DB_CONTAINER_NAME="tib-twisted-db"
DB_DATABASE="mysql"
DB_USER="mysql"
DB_PASSWORD="fgIZwgoK_OjaIe28"
DB_PORT="3306"

docker run -d \
  --name $DB_CONTAINER_NAME \
  -e MYSQL_USER="$DB_USER" \
  -e MYSQL_PASSWORD="$DB_PASSWORD" \
  -e MYSQL_DATABASE="$DB_DATABASE" \
  -p "$DB_PORT":3306 \
  docker.io/mysql