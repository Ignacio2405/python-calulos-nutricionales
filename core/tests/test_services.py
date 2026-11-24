"""Pruebas del servicio que coordina los indicadores."""

import pytest

from core.exceptions import DatosInsuficientesError
from core.schemas import CalculoAntropometriaRequest
from core.services import AntropometriaService


def test_servicio_armar_resultados_manuales(
    solicitud_completa: dict[str, object],
) -> None:
    # 1) Los resultados se comparan con los cálculos manuales documentados en SPEC §8.
    request = CalculoAntropometriaRequest.model_validate(solicitud_completa)
    resultados = AntropometriaService.calcular(request)

    assert resultados.model_dump() == {
        "imc": 25.16,
        "porcentajeMG": 30.4,
        "porcentajeMM": 32.1,
        "mBasal": 1395.3,
        "bodyAge": None,
        "grVisceral": 1.08,
        "icc": 0.78,
    }


def test_servicio_preservar_indicadores_independientes() -> None:
    # 1) Solo cintura y cadera alcanzan para calcular ICC; los demás quedan en null.
    request = CalculoAntropometriaRequest.model_validate(
        {"mediciones": {"cintura": 76, "cadera": 98}}
    )
    resultados = AntropometriaService.calcular(request)

    assert resultados.icc == 0.78
    assert resultados.imc is None
    assert resultados.mBasal is None
    assert resultados.porcentajeMG is None
    assert resultados.porcentajeMM is None
    assert resultados.grVisceral is None
    assert resultados.bodyAge is None


def test_servicio_rechazar_resultados_todos_nulos() -> None:
    # 1) Una medición sin indicadores calculables no genera un 200 vacío.
    request = CalculoAntropometriaRequest.model_validate(
        {"mediciones": {"cuello": 33}}
    )
    with pytest.raises(DatosInsuficientesError):
        AntropometriaService.calcular(request)
