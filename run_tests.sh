#!/usr/bin/env bash
docker-compose build
docker-compose up -d postgres
sleep 10
docker-compose run --rm scraper mypy ./nasdaq_analytics/
docker-compose run --rm scraper flake8 ./nasdaq_analytics/
