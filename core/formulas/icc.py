"""Cálculo del índice cintura-cadera."""

from core.math_utils import dividir_seguro


def calcular_icc(cintura: float | None, cadera: float | None) -> float | None:
    """Calculá ICC = cintura / cadera; ambas medidas en cm, salida adimensional.

    Referencia: World Health Organization. Waist circumference and waist-hip
    ratio: report of a WHO expert consultation, Geneva, 8-11 December 2008.
    Geneva: WHO; 2011.
    Validez: cintura y cadera deben ser positivas; el SPEC no fija un intervalo
    de interpretación ni una población clínica específica.
    """
    if cintura is None or cadera is None or cintura <= 0 or cadera <= 0:
        return None
    return dividir_seguro(cintura, cadera)
