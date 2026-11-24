"""Configuración del servicio desde variables de entorno."""

import logging
import logging.config
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DEBUG = os.getenv("DEBUG", "False") == "True"
API_TOKEN = os.getenv("API_TOKEN", "").strip()

try:
    PORT = int(os.getenv("PORT", "8000"))
except ValueError as exc:
    raise ValueError("PORT debe ser un número entero.") from exc

if not 1 <= PORT <= 65535:
    raise ValueError("PORT debe estar entre 1 y 65535.")

LOG_LEVEL_NAME = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = logging.getLevelNamesMapping().get(LOG_LEVEL_NAME)
if not isinstance(LOG_LEVEL, int):
    raise ValueError("LOG_LEVEL debe ser un nivel de logging válido.")

if not DEBUG and not API_TOKEN:
    raise RuntimeError("API_TOKEN es obligatorio cuando DEBUG no está activo.")

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "[{asctime}] {levelname} {name}: {message}",
                "style": "{",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "simple",
            }
        },
        "root": {"handlers": ["console"], "level": LOG_LEVEL},
    }
)

if DEBUG and not API_TOKEN:
    logging.getLogger(__name__).warning(
        "La autenticación X-API-Key está desactivada porque DEBUG está activo."
    )
