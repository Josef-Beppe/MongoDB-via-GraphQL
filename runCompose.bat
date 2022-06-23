set COMPOSE_CONVERT_WINDOWS_PATHS=1
docker-compose -p Mongodb_via_GraphQL up -d --build
pause
docker-compose -p Mongodb_via_GraphQL down