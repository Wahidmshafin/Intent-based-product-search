<<<<<<< HEAD
# Intent Based Product Search
=======
# backend
>>>>>>> 6892cdb94693989099eb7dac1ed446cf219a2855

This project was generated using fastapi_template.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m backend
```

<<<<<<< HEAD
This will start the server on the configured host. Remember, We are using Gunicorn for running the project, it can't be run on windows. If we must run it on windows, we need to setup linux subsystem for windows.

You can find swagger documentation at `/api/docs`.

### Install any library (for example numpy)
=======
This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

## 1. Install any library (For example numpy)
>>>>>>> 6892cdb94693989099eb7dac1ed446cf219a2855

Simply run:

```bash
poetry add numpy
```

- This command downloads and installs the latest compatible NumPy wheel into your project’s virtual environment.  
- Poetry will automatically insert a line under `[tool.poetry.dependencies]` in **pyproject.toml** (and update your `poetry.lock`) for you. citeturn1search2  



If you ever edit `pyproject.toml` by hand—whether you’ve tweaked version bounds, added extras, or moved dependencies between groups—keep everything consistent by running:

```bash
poetry lock --no-update
poetry install
```

- `poetry lock --no-update` regenerates `poetry.lock` to match your `pyproject.toml` without pulling in newer versions of unrelated packages.  
- `poetry install` then ensures your virtual environment matches the updated lockfile. citeturn2search0  

---

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose up --build
```

If you want to develop in docker with autoreload and exposed ports add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose build
```

## Project structure

```bash
$ tree "backend"
backend
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifespan.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here. 

All environment variables should start with "BACKEND_" prefix.

For example if you see in your "backend/settings.py" a variable named like
`random_parameter`, you should provide the "BACKEND_RANDOM_PARAMETER" 
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `backend.settings.Settings.Config`.

An example of .env file:
```bash
BACKEND_RELOAD="True"
BACKEND_PORT="8000"
BACKEND_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* ruff (spots possible bugs);


You can read more about pre-commit here: https://pre-commit.com/

## Kubernetes
To run your app in kubernetes
just run:
```bash
kubectl apply -f deploy/kube
```

It will create needed components.

If you haven't pushed to docker registry yet, you can build image locally.

```bash
docker-compose build
docker save --output backend.tar backend:latest
```


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose run --build --rm api pytest -vv .
docker-compose down
```

For running tests on your local machine.
1. you need to start a database.

I prefer doing it with docker:
```
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=backend" -e "POSTGRES_USER=backend" -e "POSTGRES_DB=backend" postgres:16.3-bullseye
```


2. Run the pytest.
```bash
pytest -vv .
```
