# src/core/exceptions/base/base_exception_handler.py

from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class ExceptionHandler:

    @staticmethod
    async def handler(request: Request, exc: HTTPException) -> JSONResponse:
        response = JSONResponse(
            status_code=exc.status_code,
            content={
                "status_code": str(exc.status_code),
                "status_name": HTTPStatus(exc.status_code).phrase,
                "message": exc.detail,
            },
        )

        return response
