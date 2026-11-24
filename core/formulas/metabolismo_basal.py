"""Cálculo del metabolismo basal por Mifflin-St Jeor."""

import math

SEXO_MASCULINO = "M"
EDAD_ADULTA_MINIMA = 18
COEFICIENTE_PESO = 10
COEFICIENTE_TALLA = 6.25
COEFICIENTE_EDAD = 5
AJUSTE_MASCULINO = 5
AJUSTE_FEMENINO = -161


def calcular_metabolismo_basal(
    peso: float | None,
    talla: float | None,
    edad: int | None,
    sexo: str | None,
) -> float | None:
    """Calculá TMB = 10·peso + 6.25·talla − 5·edad + s.

    Entradas: peso en kg, talla en cm, edad en años y sexo M/F. Salida: kcal/día.
    Referencia: Mifflin MD, St Jeor ST, Hill LA, Scott BJ, Daugherty SA, Koh YO.
    A new predictive equation for resting energy expenditure in healthy
    individuals. Am J Clin Nutr. 1990;51(2):241-247.
    Aplicabilidad: adultos de 18 años o más; fuera de ese rango se devuelve None.
    """
    if peso is None or talla is None or edad is None or sexo not in ("M", "F"):
        return None
    if (
        not math.isfinite(peso)
        or not math.isfinite(talla)
        or peso <= 0
        or talla <= 0
        or edad < EDAD_ADULTA_MINIMA
    ):
        return None

    ajuste = AJUSTE_MASCULINO if sexo == SEXO_MASCULINO else AJUSTE_FEMENINO
    resultado = (
        COEFICIENTE_PESO * peso
        + COEFICIENTE_TALLA * talla
        - COEFICIENTE_EDAD * edad
        + ajuste
    )
    return resultado if math.isfinite(resultado) else None
