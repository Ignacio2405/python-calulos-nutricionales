"""Conversiones y operaciones numéricas compartidas por las fórmulas."""

import math
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENTIMETROS_POR_METRO = 100
MILIMETROS_POR_CENTIMETRO = 10


def cm_a_m(valor_cm: float | None) -> float | None:
    """Convertí centímetros a metros."""
    if valor_cm is None or not math.isfinite(valor_cm):
        return None
    return valor_cm / CENTIMETROS_POR_METRO


def mm_a_cm(valor_mm: float | None) -> float | None:
    """Convertí milímetros a centímetros."""
    if valor_mm is None or not math.isfinite(valor_mm):
        return None
    return valor_mm / MILIMETROS_POR_CENTIMETRO


def dividir_seguro(numerador: float | None, denominador: float | None) -> float | None:
    """Dividí valores finitos; devolvé None si el divisor no sirve."""
    if numerador is None or denominador is None:
        return None
    if not math.isfinite(numerador) or not math.isfinite(denominador) or denominador == 0:
        return None
    resultado = numerador / denominador
    return resultado if math.isfinite(resultado) else None


def redondear(valor: float | None, decimales: int) -> float | None:
    """Redondeá con ROUND_HALF_UP, preservando los valores no disponibles."""
    if valor is None:
        return None
    if decimales < 0:
        raise ValueError("La cantidad de decimales no puede ser negativa.")
    if not math.isfinite(valor):
        return None
    cuantizador = Decimal("1").scaleb(-decimales)
    try:
        return float(Decimal(str(valor)).quantize(cuantizador, rounding=ROUND_HALF_UP))
    except InvalidOperation as exc:
        raise ValueError("No se pudo redondear el valor.") from exc
