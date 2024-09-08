## Web Application example of a Full Stack Project

### Project structure

     ├── src                                 Source code of the Web App
     ├── tests
     |    ├── infra                          Tests infrastructure (tests building blocks)
     |    |    ├── page-elements             Models of the elements used for building page objects
     |    |    └── page-objects              Model of the Web App pages used for building tests
     |    |
     |    └── tests                          Tests spec files
     |
     ├── run-e2e-tests.sh                    Script of E2E tests running (with the real API server)
     ├── run-mocked-tests.sh                 Script of running tests with mocked API server
     ├── Dockerfile                          Docker file of the Web App 
     └── docker-compose.yaml                 Composition of the Web App and the API Server

### Installation

`npm install`

### Tests local run with mocked API server

Start the Web App: `npm run build && npm run start`  
Run tests: `npm run tests:mocked` (at the first time you'll be asked to install browsers for playwright)

### Tests run in Docker

Run tests with the mocked API Server: `./run-mocked-tests.sh`  
Run E2E tests with the real API Server: `./run-e2e-tests.sh`