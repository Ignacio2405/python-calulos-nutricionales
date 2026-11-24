"""Cálculo del índice de masa corporal."""

from core.math_utils import cm_a_m, dividir_seguro

EXPONENTE_TALLA = 2


def calcular_imc(peso: float | None, talla: float | None) -> float | None:
    """Calculá IMC = peso / talla_m²; peso en kg, talla en cm y salida en kg/m².

    Referencia: Quetelet (índice peso/estatura²); World Health Organization.
    Obesity: preventing and managing the global epidemic. WHO Technical Report
    Series 894. Geneva: WHO; 2000.
    Validez: la fórmula requiere peso y talla positivos; el SPEC no fija un
    intervalo de interpretación ni una población clínica específica.
    """
    talla_m = cm_a_m(talla)
    if peso is None or talla_m is None or peso <= 0 or talla_m <= 0:
        return None
    return dividir_seguro(peso, talla_m**EXPONENTE_TALLA)
