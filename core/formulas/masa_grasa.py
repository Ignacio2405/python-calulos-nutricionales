"""Cálculo del porcentaje de masa grasa por Durnin-Womersley y Siri."""

import math

COEFICIENTES_DURNIN_WOMERSLEY = {
    (17, 19): {"M": (1.1620, 0.0630), "F": (1.1549, 0.0678)},
    (20, 29): {"M": (1.1631, 0.0632), "F": (1.1599, 0.0717)},
    (30, 39): {"M": (1.1422, 0.0544), "F": (1.1423, 0.0632)},
    (40, 49): {"M": (1.1620, 0.0700), "F": (1.1333, 0.0612)},
    (50, 72): {"M": (1.1715, 0.0779), "F": (1.1339, 0.0645)},
}
FACTOR_SIRI = 495
AJUSTE_SIRI = 450
EDAD_MINIMA = 17
EDAD_MAXIMA = 72
PORCENTAJE_MINIMO = 0
PORCENTAJE_MAXIMO = 100


def calcular_porcentaje_mg(
    sexo: str | None,
    edad: int | None,
    p_bicipital: float | None,
    p_tricipital: float | None,
    p_subescapular: float | None,
    p_suprailiaco: float | None,
) -> float | None:
    """Calculá %MG = 495 / D − 450, con D = c − m·log10(S).

    Entradas: sexo M/F, edad en años y cuatro pliegues en mm; salida en porcentaje.
    Referencias: Durnin JVGA, Womersley J. Body fat assessed from total body
    density and its estimation from skinfold thickness: measurements on 481 men
    and women aged from 16 to 72 years. Br J Nutr. 1974;32(1):77-97. Siri WE.
    Body composition from fluid spaces and density. In: Brozek J, Henschel A,
    editors. Techniques for Measuring Body Composition. Washington, DC: National
    Academy of Sciences; 1961. p. 223-244.
    Aplicabilidad: adultos de 17 a 72 años con medición estandarizada de los
    cuatro pliegues; la estimación tiene error respecto de métodos de referencia.
    """
    insumos = (
        sexo,
        edad,
        p_bicipital,
        p_tricipital,
        p_subescapular,
        p_suprailiaco,
    )
    if any(valor is None for valor in insumos):
        return None
    if sexo not in ("M", "F") or edad is None or not EDAD_MINIMA <= edad <= EDAD_MAXIMA:
        return None

    pliegues = (p_bicipital, p_tricipital, p_subescapular, p_suprailiaco)
    if any(valor is None or valor < 0 for valor in pliegues):
        return None
    suma_pliegues = sum(pliegues)
    if suma_pliegues <= 0:
        return None

    coeficientes = next(
        (
            valores[sexo]
            for (edad_minima, edad_maxima), valores in COEFICIENTES_DURNIN_WOMERSLEY.items()
            if edad_minima <= edad <= edad_maxima
        ),
        None,
    )
    if coeficientes is None:
        return None

    constante, pendiente = coeficientes
    densidad = constante - pendiente * math.log10(suma_pliegues)
    if densidad <= 0:
        return None

    porcentaje = FACTOR_SIRI / densidad - AJUSTE_SIRI
    if not PORCENTAJE_MINIMO <= porcentaje <= PORCENTAJE_MAXIMO:
        return None
    return porcentaje
