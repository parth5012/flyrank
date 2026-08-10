## start a container/pull image with mounted volume
docker run --name taskdb -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=tasks -p 5432:5432 -v taskdata:/var/lib/postgresql -d postgres
## Delete container and volume
docker rm -f taskdb
docker volume rm taskdata
## Run psql cli
docker exec -it taskdb psql -U postgres -d tasks
## Check container logs
docker logs -f taskdb
## Check running containers
docker ps
## Check container status
docker inspect taskdb
## Check Tables in db instance
docker exec -it taskdb psql -U postgres -d tasks -c "\dt"


## Test tasks get endpoint
curl -i http://localhost:3000/tasks

## Run the project
docker compose up --build -d

## Stop the project
docker compose down
