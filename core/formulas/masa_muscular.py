"""Cálculo del porcentaje de masa muscular esquelética."""

import math

from core.math_utils import dividir_seguro, mm_a_cm

CORRECCION_AREA_MASCULINA = 10
CORRECCION_AREA_FEMENINA = 6.5
EDAD_ADULTA_MINIMA = 18
COEFICIENTE_ALTURA = 0.0264
COEFICIENTE_AREA_MUSCULAR = 0.0029
FACTOR_PORCENTAJE = 100
FACTOR_AREA_CIRCULAR = 4
PORCENTAJE_MINIMO = 0
PORCENTAJE_MAXIMO = 100
PI = math.pi


def calcular_porcentaje_mm(
    peso: float | None,
    talla: float | None,
    brazo: float | None,
    p_tricipital: float | None,
    sexo: str | None,
    edad: int | None,
) -> float | None:
    """Calculá %MM usando el área muscular del brazo corregida por hueso.

    TSF_cm = pTricipital_mm / 10; CAMA = (brazo_cm − π·TSF_cm)²/(4π) − k;
    MME_kg = talla_cm·(0.0264 + 0.0029·CAMA); %MM = 100·MME/peso_kg.
    Entradas: peso en kg, talla y brazo en cm, pliegue tricipital en mm, sexo M/F
    y edad en años. Salida: porcentaje de masa muscular esquelética.
    Referencia: Heymsfield SB, McManus C, Smith J, Stevens V, Nixon DW.
    Anthropometric measurement of muscle mass: revised equations for calculating
    bone-free arm muscle area. Am J Clin Nutr. 1982;36(4):680-690.
    Aplicabilidad: adultos de 18 años o más. Estima músculo esquelético desde un
    único sitio y no equivale a masa magra ni masa libre de grasa.
    """
    insumos = (peso, talla, brazo, p_tricipital, sexo, edad)
    if any(valor is None for valor in insumos):
        return None
    if (
        peso is None
        or talla is None
        or brazo is None
        or p_tricipital is None
        or sexo not in ("M", "F")
        or edad is None
        or edad < EDAD_ADULTA_MINIMA
        or peso <= 0
        or talla <= 0
        or brazo <= 0
        or p_tricipital < 0
    ):
        return None

    pliegue_cm = mm_a_cm(p_tricipital)
    if pliegue_cm is None:
        return None
    circunferencia_muscular = brazo - PI * pliegue_cm
    if circunferencia_muscular <= 0:
        return None

    correccion = (
        CORRECCION_AREA_MASCULINA if sexo == "M" else CORRECCION_AREA_FEMENINA
    )
    area_muscular_corregida = (
        circunferencia_muscular**2 / (FACTOR_AREA_CIRCULAR * PI) - correccion
    )
    if area_muscular_corregida <= 0:
        return None

    masa_muscular = talla * (
        COEFICIENTE_ALTURA + COEFICIENTE_AREA_MUSCULAR * area_muscular_corregida
    )
    porcentaje = dividir_seguro(FACTOR_PORCENTAJE * masa_muscular, peso)
    if porcentaje is None or not PORCENTAJE_MINIMO <= porcentaje <= PORCENTAJE_MAXIMO:
        return None
    return porcentaje
