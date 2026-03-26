#!/bin/bash
docker-compose up -d
echo "Started!"
docker-compose exec web flask db upgrade