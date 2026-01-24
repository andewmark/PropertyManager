#!/bin/bash

docker-compose down -v
docker-compose up -d

sleep 5
docker-compose exec web flask db upgrade
docker cp seed.sql property-management-db-1:seed.sql
docker-compose exec db psql -U dev test_db -f seed.sql
echo "Setup Complete!"