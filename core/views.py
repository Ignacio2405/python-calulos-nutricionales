"""Endpoints HTTP del módulo, sin lógica matemática."""

from fastapi import APIRouter, Depends

from core.schemas import CalculoAntropometriaRequest, CalculoAntropometriaResponse
from core.security import verificar_api_key
from core.services import AntropometriaService

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "Calculos Nutricionales"}


@router.post(
    "/calcular-antropometria",
    response_model=CalculoAntropometriaResponse,
)
def calcular_antropometria(
    request: CalculoAntropometriaRequest,
    _: None = Depends(verificar_api_key),
) -> CalculoAntropometriaResponse:
    resultados = AntropometriaService.calcular(request)
    return CalculoAntropometriaResponse(resultados=resultados)
