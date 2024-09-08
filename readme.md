# Customer FastAPI
This is a FastAPI API endpoint that is designed to be spun up in a docker container.

## Run the application
To run the application, make sure you have Docker installed. More information is available here:
https://docs.docker.com/engine/install/

You can then run the startup.sh script on Mac/Linux machines to start the container.

You can use docker compose to build the container on windows machines:
```bash
docker-compose build

docker-compose up -d
```
## Documentation
Once the container is running the documentation can be found at the /ui endpoint.

### Notes
The end point uses a postgre database to store various customer information, for specifics please see the openapi.yaml file

This was written in 5 days, and single handedly! As I was in an arm sling.
