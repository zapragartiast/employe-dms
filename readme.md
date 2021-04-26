# Employees Data Management System API  
Built with Python Flask. This project just handling the JSON REST API without any administration dashboard or others views.  
  
You can simply `pull` or `clone` this project.

Currently this project have no documentation. This project is just for fun! 🤣

## Quick Start Guide  
After you clone this project, run `docker build .` then `docker-compose up`. After the project running inside Docker container, visit `http://localhost:5000` to start use the API.

## Run Tests
There's a Dockerfile named `Dockerfile.test` and docker-compose named `docker-compose.test.yml`. You can start the test using the command below.
```
docker-compose -f docker-compose.test.yml up --build \
    --abort-on-container-exit \
    --exit-code-from app
```
After the test complete, the test container will exit immediately.

## Issues
Please [open issue](https://github.com/zapragartiast/employe-dms/issues/new) if you get a troubles.