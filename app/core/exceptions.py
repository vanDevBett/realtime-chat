from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def add_exception_handlers(app: FastAPI):

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc)
            }
        )

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not found",
                "detail": "The requested resource was not found"
            }
        )