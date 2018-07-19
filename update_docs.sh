#!/usr/bin/env bash
docker-compose build
docker-compose up -d postgres
sleep 10
docker-compose run --rm scraper bash -c "sphinx-apidoc -o docs/ nasdaq_analytics ; cd docs/ ; make html;"