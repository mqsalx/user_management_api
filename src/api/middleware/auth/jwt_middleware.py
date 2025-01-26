# /src/api/middleware/auth/jwt_middleware.py


from math import e
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.configurations.env_configuration import EnvConfiguration
from src.core.exceptions.base.base_exception import BaseException
from src.utils.auth.jwt_util import verify_token
from src.utils.log.console_logger_util import ConsoleLoggerUtil

# Env variables Setup
API_VERSION = EnvConfiguration().api_version

# Log variables Setup
logger_error = ConsoleLoggerUtil().log_error


class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:

            if request.url.path in [
                f"/api-{API_VERSION}/login",
                "/docs",
                "/openapi.json",
            ]:
                return await call_next(request)

            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise BaseException("Token not provided!")

            token = auth_header.split(" ")[1]

            try:
                verify_token(token)
            except ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expired!")
            except InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token!")

            return await call_next(request)
        except Exception as error:

            logger_error(f"Token validation error: {error}")

            return self.__json_response(error)


    def __json_response(self, exception) -> JSONResponse:
        return JSONResponse(
            status_code=exception.status_code,
            content=exception.message,
        )

    # except BaseHTTPException as error:

    #     logger_error(f"Token validation error: {error}")

    #     raise error
