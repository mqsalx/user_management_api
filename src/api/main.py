# /src/api/main.py

"""
Main module responsible for initializing and running the FastAPI application.

This module sets up the API, middleware, exception handlers, and scheduled tasks.
It also checks environment variables and the database connection before starting
the server.
"""

import time

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from src.api.routes import login_router, user_router
from src.api.routes import system_router
from src.core.configurations.env_configuration import EnvConfiguration
from src.core.exceptions.exception_handler import ExceptionHandler
from src.core.middleware.auth_middleware import AuthMiddleware
from src.core.middleware.logger_middleware import LoggerMiddleware
from src.usecases.scheduler_usecase import Scheduler
from src.utils.database_util import DatabaseUtil
from src.utils.dot_env_util import DotEnvUtil
from src.utils.logger_util import LoggerUtil
from src.utils.message_util import MessageUtil

app = FastAPI()
log = LoggerUtil()

# Env variables Setup
API_HOST = EnvConfiguration().api_host
API_NAME = EnvConfiguration().api_name
API_PORT = EnvConfiguration().api_port
API_VERSION = EnvConfiguration().api_version


def my_function():
    """
    Standalone function responsible for testing scheduled tasks.

    This function logs a test message with the current timestamp.

    Args:
        None

    Returns:
        None
    """

    log.info(f"Testing... {time.strftime("%Y-%m-%d %H:%M:%S")}")


my_scheduler_task = Scheduler()

# my_scheduler_task.schedule_function(my_function, 5)

app.add_exception_handler(HTTPException, ExceptionHandler.http_exception_handler)  # type: ignore
app.add_exception_handler(RequestValidationError, ExceptionHandler.json_decode_error_handler)  # type: ignore

app.add_middleware(LoggerMiddleware)
app.add_middleware(AuthMiddleware)

routers = [(user_router.router, "/users"), (login_router.router, "/login")]

for router, prefix in routers:
    app.include_router(router, prefix=f"/api-{API_VERSION}{prefix}")

app.include_router(system_router.router, prefix="/api/system")

if __name__ == "__main__":
    """
    Application startup sequence.

    This section ensures that essential configurations are checked before
    running the FastAPI server.
    """

    # On Startup Message
    MessageUtil().on_startup()

    # Check ENV variables
    DotEnvUtil().check_dot_env()

    # Check Database Connection
    DatabaseUtil().check_connection()

    width = 80
    border = "=" * width

    uvicorn.run(app, host=API_HOST, port=API_PORT, log_config=None)
