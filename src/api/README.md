## API Server example of a Full Stack Application

### Project structure

     ├── src                                 Source code of the API server
     ├── tests
     |    ├── functional                     Functional tests
     |    └── unit                           Unit tests
     └── api-server.sh                       Local Starting/Stopping the API server

### To install the project

1. Install the Python ver as in .python-version: `pyenv install`
2. Install the virtual env to .venv: `python -m venv .venv`
3. Activate the virtual env: `source .venv/bin/activate`
4. Install poetry: `pip install poetry`
5. Select the virtual env for poetry: `poetry env use .venv/bin/python`
6. Install the dependencies: `poetry install --no-root`

### To run tests (no need to start the API server separately)

- Unit tests: `tox run -e unit`
- Functional tests: `tox run -e functional`

### To run API server locally (as a background process)

- Start: `./api-server.sh start`
- Stop: `./api-server.sh stop`

### To run API server in a Docker container (as a background process)

1. Build the Docker image: `docker build -t api-server .`
2. Run the image: `docker run -p 8000:8000 --name api-server -d api-server:latest`

### Used libraries

- [Poetry](https://python-poetry.org/) - is a tool for dependency management and packaging in Python
- [Tox](https://tox.wiki/) - to automate and standardize testing in Python
- [Falcon](https://falconframework.org/) - is a minimalist ASGI/WSGI framework for building mission-critical REST APIs
  and microservices, with a
  focus on reliability, correctness, and performance at scale
- [Pytest](https://pytest.org) - framework makes it easy to write small, readable tests, and can scale to support
  complex functional testing
  for applications and libraries