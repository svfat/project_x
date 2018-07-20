#!/usr/bin/env bash
docker-compose build
docker-compose up -d postgres
docker-compose run --rm wait-for-postgres
docker-compose run --rm scraper bash -c "sphinx-apidoc -o docs/ nasdaq_analytics ; cd docs/ ; make html;"