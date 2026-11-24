"""Autenticación del servicio compartida con Node.js."""

import hmac

from fastapi import Header

from config.settings import API_TOKEN, DEBUG
from core.exceptions import NoAutorizadoError


def verificar_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    """Exigí X-API-Key salvo en desarrollo con token vacío."""
    if DEBUG and not API_TOKEN:
        return
    if x_api_key is None or not hmac.compare_digest(
        x_api_key.encode("utf-8"),
        API_TOKEN.encode("utf-8"),
    ):
        raise NoAutorizadoError
