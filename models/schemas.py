from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ParametroClimatico(str, Enum):
    temperature_2m = "temperature_2m"
    relative_humidity_2m = "relative_humidity_2m"
    surface_pressure = "surface_pressure"
    wind_speed_10m = "wind_speed_10m"
    wind_direction_10m = "wind_direction_10m"
    precipitation = "precipitation"


class FiltroTempoQuery(BaseModel):
    cidade: str = Field(
        default="Belo Horizonte",
        min_length=2,
        max_length=100,
        description="Nome da cidade para consulta",
    )
    dias: int = Field(
        default=7,
        ge=1,
        description="Quantidade de dias para consulta",
    )
    parametros: Optional[List[ParametroClimatico]] = Field(
        default=None,
        description="Lista de variáveis climáticas desejadas (ex: ?parametros=temperature_2m&parametros=precipitation)",
    )

class CityCollect(BaseModel):
    city: str
    days: int
