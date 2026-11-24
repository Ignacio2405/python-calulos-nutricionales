"""Modelos de entrada y salida del contrato HTTP."""

import re
from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    ValidationInfo,
    field_validator,
    model_validator,
)

PESO_MIN = 2.0
PESO_MAX = 500.0
TALLA_MIN = 30.0
TALLA_MAX = 272.0
CUELLO_MIN = 10.0
CUELLO_MAX = 80.0
BRAZO_MIN = 5.0
BRAZO_MAX = 80.0
CINTURA_MIN = 20.0
CINTURA_MAX = 250.0
CADERA_MIN = 30.0
CADERA_MAX = 250.0
PLIEGUE_MIN = 0.0
PLIEGUE_MAX = 80.0

_FECHA_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_MEDICIONES_POSITIVAS = {"peso", "talla", "cuello", "brazo", "cintura", "cadera"}


def _edad_en_fecha(fecha_nacimiento: date, fecha_referencia: date) -> int:
    """Calculá los años cumplidos a la fecha de referencia."""
    return fecha_referencia.year - fecha_nacimiento.year - (
        (fecha_referencia.month, fecha_referencia.day)
        < (fecha_nacimiento.month, fecha_nacimiento.day)
    )


def _error_de_edad(valor: object, mensaje: str) -> ValidationError:
    return ValidationError.from_exception_data(
        title="DatosPacienteInput",
        line_errors=[
            {
                "type": "value_error",
                "loc": ("edad",),
                "input": valor,
                "ctx": {"error": ValueError(mensaje)},
            }
        ],
    )


class DatosPacienteInput(BaseModel):
    """Datos demográficos opcionales usados por algunas fórmulas."""

    model_config = ConfigDict(extra="forbid")

    sexo: Literal["M", "F"] | None = None
    fechaNacimiento: date | None = None
    edad: Annotated[int, Field(ge=0, le=120, strict=True)] | None = None

    @field_validator("fechaNacimiento", mode="before")
    @classmethod
    def validar_formato_fecha(cls, valor: object) -> object:
        if valor is None:
            return None
        if isinstance(valor, datetime):
            raise ValueError("Ingresá la fecha en formato YYYY-MM-DD.")
        if isinstance(valor, date):
            return valor
        if not isinstance(valor, str) or not _FECHA_ISO.fullmatch(valor):
            raise ValueError("Ingresá la fecha en formato YYYY-MM-DD.")
        try:
            return date.fromisoformat(valor)
        except ValueError as exc:
            raise ValueError("Ingresá una fecha válida.") from exc

    @field_validator("fechaNacimiento")
    @classmethod
    def rechazar_fecha_futura(cls, valor: date | None) -> date | None:
        if valor is not None and valor > date.today():
            raise ValueError("La fecha de nacimiento no puede ser futura.")
        return valor

    @model_validator(mode="after")
    def validar_y_derivar_edad(self) -> "DatosPacienteInput":
        if self.fechaNacimiento is None:
            return self

        edad_derivada = _edad_en_fecha(self.fechaNacimiento, date.today())
        if self.edad is not None:
            if abs(edad_derivada - self.edad) > 1:
                raise _error_de_edad(
                    self.edad,
                    "La edad no coincide con la fecha de nacimiento.",
                )
            return self

        if not 0 <= edad_derivada <= 120:
            raise _error_de_edad(
                edad_derivada,
                "La edad derivada debe estar entre 0 y 120 años.",
            )
        self.edad = edad_derivada
        return self


class MedicionesInput(BaseModel):
    """Mediciones opcionales, expresadas en las unidades del contrato."""

    model_config = ConfigDict(extra="forbid")

    peso: float | None = Field(default=None, ge=PESO_MIN, le=PESO_MAX, allow_inf_nan=False)
    talla: float | None = Field(default=None, ge=TALLA_MIN, le=TALLA_MAX, allow_inf_nan=False)
    cuello: float | None = Field(default=None, ge=CUELLO_MIN, le=CUELLO_MAX, allow_inf_nan=False)
    brazo: float | None = Field(default=None, ge=BRAZO_MIN, le=BRAZO_MAX, allow_inf_nan=False)
    cintura: float | None = Field(default=None, ge=CINTURA_MIN, le=CINTURA_MAX, allow_inf_nan=False)
    cadera: float | None = Field(default=None, ge=CADERA_MIN, le=CADERA_MAX, allow_inf_nan=False)
    pTricipital: float | None = Field(default=None, ge=PLIEGUE_MIN, le=PLIEGUE_MAX, allow_inf_nan=False)
    pBicipital: float | None = Field(default=None, ge=PLIEGUE_MIN, le=PLIEGUE_MAX, allow_inf_nan=False)
    pSubescapular: float | None = Field(default=None, ge=PLIEGUE_MIN, le=PLIEGUE_MAX, allow_inf_nan=False)
    pSuprailiaco: float | None = Field(default=None, ge=PLIEGUE_MIN, le=PLIEGUE_MAX, allow_inf_nan=False)

    @field_validator(
        "peso",
        "talla",
        "cuello",
        "brazo",
        "cintura",
        "cadera",
        "pTricipital",
        "pBicipital",
        "pSubescapular",
        "pSuprailiaco",
        mode="before",
    )
    @classmethod
    def validar_tipo_numerico(
        cls,
        valor: object,
        info: ValidationInfo,
    ) -> object:
        if valor is None:
            return None
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("Ingresá un valor numérico.")
        if info.field_name in _MEDICIONES_POSITIVAS and valor <= 0:
            raise ValueError("Debe ser mayor que 0.")
        return valor

    @model_validator(mode="after")
    def validar_medicion_informada(self) -> "MedicionesInput":
        if not any(getattr(self, campo) is not None for campo in type(self).model_fields):
            raise ValueError("Informá al menos una medición.")
        return self


class CalculoAntropometriaRequest(BaseModel):
    """Payload aceptado por POST /calcular-antropometria."""

    model_config = ConfigDict(extra="forbid")

    paciente: DatosPacienteInput | None = None
    mediciones: MedicionesInput


class ResultadosAntropometria(BaseModel):
    """Los siete indicadores; los no calculables se informan como null."""

    model_config = ConfigDict(extra="forbid")

    imc: float | None = None
    porcentajeMG: float | None = None
    porcentajeMM: float | None = None
    mBasal: float | None = None
    bodyAge: int | None = None
    grVisceral: float | None = None
    icc: float | None = None


class CalculoAntropometriaResponse(BaseModel):
    """Respuesta exitosa con el conjunto fijo de resultados."""

    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    resultados: ResultadosAntropometria
