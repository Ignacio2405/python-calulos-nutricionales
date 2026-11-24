"""Cálculo del índice de conicidad."""

import math

from core.math_utils import cm_a_m, dividir_seguro

COEFICIENTE_CONICIDAD = 0.109


def calcular_grasa_visceral(
    cintura: float | None,
    peso: float | None,
    talla: float | None,
) -> float | None:
    """Calculá C = cintura_m / (0.109 · √(peso / talla_m)).

    Entradas: cintura en cm, peso en kg y talla en cm. La salida es adimensional.
    Referencia: Valdez R. A simple model-based index of abdominal adiposity.
    J Clin Epidemiol. 1991;44(9):955-956.
    Validez: requiere peso, talla y cintura positivos; el SPEC no fija otros
    límites de edad o población. Es una estimación antropométrica, no un
    diagnóstico ni una medición directa de grasa visceral.
    """
    cintura_m = cm_a_m(cintura)
    talla_m = cm_a_m(talla)
    if (
        cintura_m is None
        or peso is None
        or talla_m is None
        or cintura_m <= 0
        or peso <= 0
        or talla_m <= 0
    ):
        return None

    cociente = dividir_seguro(peso, talla_m)
    if cociente is None or cociente <= 0:
        return None
    denominador = COEFICIENTE_CONICIDAD * math.sqrt(cociente)
    return dividir_seguro(cintura_m, denominador)
