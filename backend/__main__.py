import os
import shutil
from pathlib import Path

import uvicorn

from backend.gunicorn_runner import GunicornApplication
from backend.settings import settings


def set_multiproc_dir() -> None:
    """
    Sets mutiproc_dir env variable.

    This function cleans up the multiprocess directory
    and recreates it. This actions are required by prometheus-client
    to share metrics between processes.

    After cleanup, it sets two variables.
    Uppercase and lowercase because different
    versions of the prometheus-client library
    depend on different environment variables,
    so I've decided to export all needed variables,
    to avoid undefined behaviour.
    """
    shutil.rmtree(settings.prometheus_dir, ignore_errors=True)
    Path(settings.prometheus_dir).mkdir(parents=True)
    os.environ["prometheus_multiproc_dir"] = str(  # noqa: SIM112
        settings.prometheus_dir.expanduser().absolute(),
    )
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )


def set_LangSmith() -> None:
    """Setup the Langsmith environment variables"""
    os.environ["LANGSMITH_TRACING"] = settings.LANGSMITH_TRACING
    os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
    os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
    os.environ["LANGSMITH_PROJECT"] = settings.LANGSMITH_PROJECT

def main() -> None:
    """Entrypoint of the application."""
    set_multiproc_dir()
    set_LangSmith()
    if settings.reload:
        uvicorn.run(
            "backend.web.application:get_app",
            workers=settings.workers_count,
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            log_level=settings.log_level.value.lower(),
            factory=True,
        )
    else:
        # We choose gunicorn only if reload
        # option is not used, because reload
        # feature doesn't work with gunicorn workers.
        GunicornApplication(
            "backend.web.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            factory=True,
            accesslog="-",
            loglevel=settings.log_level.value.lower(),
            access_log_format='%r "-" %s "-" %Tf',
        ).run()


if __name__ == "__main__":
    main()
