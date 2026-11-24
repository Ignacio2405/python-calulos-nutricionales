"""Fixtures compartidas por las pruebas del módulo."""

from datetime import date

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def cliente(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("API_TOKEN", "test-token")

    from config.app import create_app

    return TestClient(create_app(), raise_server_exceptions=False)


@pytest.fixture
def paciente_mujer() -> dict[str, object]:
    hoy = date.today()
    try:
        nacimiento = hoy.replace(year=hoy.year - 32)
    except ValueError:
        nacimiento = hoy.replace(year=hoy.year - 32, day=28)
    return {
        "sexo": "F",
        "edad": 32,
        "fechaNacimiento": nacimiento.isoformat(),
    }


@pytest.fixture
def mediciones_completas() -> dict[str, float]:
    return {
        "peso": 68.5,
        "talla": 165,
        "cuello": 33,
        "brazo": 29,
        "cintura": 76,
        "cadera": 98,
        "pTricipital": 18,
        "pBicipital": 10,
        "pSubescapular": 16,
        "pSuprailiaco": 15,
    }


@pytest.fixture
def solicitud_completa(
    paciente_mujer: dict[str, object],
    mediciones_completas: dict[str, float],
) -> dict[str, object]:
    return {"paciente": paciente_mujer, "mediciones": mediciones_completas}
