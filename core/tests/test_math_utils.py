"""Pruebas de conversiones, división y redondeo."""

import pytest

from core.math_utils import cm_a_m, dividir_seguro, mm_a_cm, redondear


def test_convertir_cm_a_m() -> None:
    # 1) 165 cm equivalen a 1.65 m.
    assert cm_a_m(165) == pytest.approx(1.65)

    # 2) Un valor ausente sigue siendo no disponible.
    assert cm_a_m(None) is None


def test_convertir_mm_a_cm() -> None:
    # 1) 18 mm equivalen a 1.8 cm.
    assert mm_a_cm(18) == pytest.approx(1.8)

    # 2) Un valor ausente sigue siendo no disponible.
    assert mm_a_cm(None) is None


def test_dividir_seguro_evitar_divisor_cero() -> None:
    # 1) El divisor cero no provoca una excepción ni se transforma en cero.
    assert dividir_seguro(1, 0) is None

    # 2) Una división válida conserva el cociente sin redondear.
    assert dividir_seguro(76, 98) == pytest.approx(76 / 98)


def test_redondear_usar_mitad_hacia_arriba() -> None:
    # 1) El cálculo manual 1395.25, a una cifra decimal, da 1395.3.
    assert redondear(1395.25, 1) == 1395.3

    # 2) ROUND_HALF_UP también aleja del cero una mitad negativa exacta.
    assert redondear(-1.25, 1) == -1.3

    # 3) Los valores no disponibles permanecen nulos.
    assert redondear(None, 2) is None
