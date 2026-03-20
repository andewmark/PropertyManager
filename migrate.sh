#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: migration message is required"
    echo "Usage: ./migrate.sh \"your message here"\"
    exit 1
fi

docker-compose exec web flask db migrate -m "${1:-update schema}"
docker-compose exec web flask db upgrade
echo "Migration complete!"