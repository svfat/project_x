#!/usr/bin/env bash
docker-compose up -d postgres
docker-compose run --rm wait-for-postgres
docker-compose run --rm scraper ./migrations/apply.sh
docker-compose run --rm scraper
docker-compose up -d web