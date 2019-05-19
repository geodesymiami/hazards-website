# API

Endpoints
---------

For more thorough documentation on the return types, json responses format, and parameters see the API Reference file.

- `/api/<string:hazard_type_param>`
    - Returns a list of all hazards of the provided hazard_type

- `/api/satellites/<int:hazard_id_param>`
    - Returns a list of all satellites that have imaged the provided hazards_id
    
- `'/api/<string:hazard_type_param>/<int:hazard_id_param>'`
    - Returns hazard information and a list of images of the provided hazards_id


Running the API Service
-----------------------

The API service, like the other components of this system, runs inside of a docker container, configured by the `Dockerfile` in this directory.
 
 To run this component of the system separately from the database and the api services, simply run the following commands from the `project/server` directory:
 
 `docker build --tag=api src/api/Dockerfile .` 
 
 `docker run api`
 
 Note that running the api service as above may result in errors when attempting to query the database, as the database may or may not be active.
 
 To run this component in conjunction with the database and processing services, as is the expected run configuration, simply run the following command from the `project/server` directory:
 
 `docker-compose build`
 
 `docker-compose up -d`
 
 `docker-compose` unlike `docker` is used to startup and run multiple linked services at once. Because the api/database/processing routines are all interdependent, using docker-compose is the suggest means by which to run the backend components.
 