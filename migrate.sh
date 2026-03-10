#!/bin/bash

docker-compose exec web flask db migrate -m "${1:-update schema}"
docker-compose exec web flask db upgrade
echo "Migration complete!"