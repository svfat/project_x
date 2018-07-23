#!/usr/bin/env bash
docker-compose up -d postgres
docker-compose run --rm wait-for-postgres
docker-compose run --rm scraper mypy ./nasdaq_analytics/
docker-compose run --rm scraper flake8 ./nasdaq_analytics/
