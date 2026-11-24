"""Creación de la aplicación FastAPI."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.exceptions import (
    DatosInsuficientesError,
    NoAutorizadoError,
    _respuesta_error,
    manejar_datos_insuficientes,
    manejar_error_no_previsto,
    manejar_no_autorizado,
    manejar_validacion,
)
from core.urls import router


async def manejar_http_error(
    _request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    if exc.status_code == 404:
        detalle = "Ruta no encontrada."
    elif exc.status_code == 405:
        detalle = "Método no permitido."
    elif exc.status_code < 500:
        detalle = str(exc.detail)
    else:
        detalle = "Error interno del servidor."
    return _respuesta_error(exc.status_code, detalle)


def create_app() -> FastAPI:
    app = FastAPI(title="Calculos Nutricionales")
    app.include_router(router)
    app.add_exception_handler(RequestValidationError, manejar_validacion)
    app.add_exception_handler(DatosInsuficientesError, manejar_datos_insuficientes)
    app.add_exception_handler(NoAutorizadoError, manejar_no_autorizado)
    app.add_exception_handler(StarletteHTTPException, manejar_http_error)
    app.add_exception_handler(Exception, manejar_error_no_previsto)
    return app


app = create_app()
