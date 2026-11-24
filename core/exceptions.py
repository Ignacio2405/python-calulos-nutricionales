"""Excepciones y respuestas de error centralizadas."""

import logging
from collections.abc import Mapping
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

_RANGOS = {
    "peso": (2, 500, "kg"),
    "talla": (30, 272, "cm"),
    "cuello": (10, 80, "cm"),
    "brazo": (5, 80, "cm"),
    "cintura": (20, 250, "cm"),
    "cadera": (30, 250, "cm"),
    "pTricipital": (0, 80, "mm"),
    "pBicipital": (0, 80, "mm"),
    "pSubescapular": (0, 80, "mm"),
    "pSuprailiaco": (0, 80, "mm"),
    "edad": (0, 120, "años"),
}


class DatosInsuficientesError(Exception):
    """No se pudo calcular ningún indicador con los datos recibidos."""


class NoAutorizadoError(Exception):
    """Falta una clave de API válida."""


def _respuesta_error(status_code: int, detail: str | dict[str, list[str]]) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"ok": False, "error": True, "detail": detail},
    )


def _campo_desde_ubicacion(ubicacion: tuple[Any, ...]) -> str:
    partes = [str(parte) for parte in ubicacion if parte not in ("body", "__root__")]
    return ".".join(partes) or "body"


def _mensaje_validacion(error: Mapping[str, Any]) -> str:
    tipo = str(error.get("type", ""))
    ubicacion = tuple(error.get("loc", ()))
    campo = str(ubicacion[-1]) if ubicacion else ""
    contexto = error.get("ctx") or {}

    if tipo == "missing":
        return "Este campo es obligatorio."
    if tipo == "extra_forbidden":
        return "Esta clave no está permitida."
    if tipo == "literal_error":
        return "Debe ser 'M' o 'F'."
    if tipo in {"float_type", "int_type"}:
        return "Ingresá un valor numérico." if tipo == "float_type" else "Ingresá un número entero."
    if tipo in {"finite_number", "finite_number_required"}:
        return "Ingresá un número finito."
    if tipo in {"greater_than", "greater_than_equal", "less_than", "less_than_equal"}:
        if campo in _RANGOS:
            minimo, maximo, unidad = _RANGOS[campo]
            return f"Debe estar entre {minimo:g} y {maximo:g} {unidad}."
        if tipo == "greater_than":
            return "Debe ser mayor que 0."
        return "El valor está fuera del rango permitido."
    if tipo in {"date_from_datetime_parsing", "date_parsing", "date_type"}:
        return "Ingresá una fecha válida en formato YYYY-MM-DD."
    if tipo == "json_invalid":
        return "El cuerpo debe ser un JSON válido."
    if tipo == "value_error":
        causa = contexto.get("error")
        if isinstance(causa, ValueError):
            return str(causa)
    return "El valor no es válido."


async def manejar_validacion(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errores: dict[str, list[str]] = {}
    for error in exc.errors():
        campo = _campo_desde_ubicacion(tuple(error.get("loc", ())))
        errores.setdefault(campo, []).append(_mensaje_validacion(error))
    return _respuesta_error(422, errores)


async def manejar_datos_insuficientes(
    _request: Request,
    _exc: DatosInsuficientesError,
) -> JSONResponse:
    return _respuesta_error(
        422,
        "No hay datos suficientes para calcular ningún indicador.",
    )


async def manejar_no_autorizado(
    _request: Request,
    _exc: NoAutorizadoError,
) -> JSONResponse:
    return _respuesta_error(401, "No autorizado.")


async def manejar_error_no_previsto(_request: Request, _exc: Exception) -> JSONResponse:
    logger.exception("Error interno al procesar una solicitud.")
    return _respuesta_error(500, "Error interno del servidor.")
