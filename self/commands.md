docker build -t self-bot .




docker run -d --name redis-db -p 6380:6379 redis:latest
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-db
