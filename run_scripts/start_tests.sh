docker compose -f ../docker-compose.yaml --profile test run --rm api_test
docker compose -f ../docker-compose.yaml --profile test down --volumes
