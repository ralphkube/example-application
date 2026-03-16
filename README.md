# example-application


## docker example

```
docker network create example

cd frontend
docker build -t frontend .
docker run --name frontend --network example --rm --env BACKEND_URL="http://backend" -p 8081:80 frontend

cd backend
docker build -t backend .
docker run --name backend --network example --rm --env REDIS_HOST=redis backend

docker run -d --rm --name redis --network example redis
```
