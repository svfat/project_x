#!/usr/bin/env bash
docker-compose build
docker-compose up -d postgres
sleep 10
docker-compose run scraper mypy ./nasdaq_analytics/
docker-compose run scraper flake8 ./nasdaq_analytics/
