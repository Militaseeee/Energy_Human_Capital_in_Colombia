# queries/__init__.py
from .analytics import (
    get_coevolucion_nacional,
    get_distribucion_regional,
    get_mapa_colombia,
    get_top_areas_conocimiento,
    get_modelo_estadistico,
    get_resource_types_diagnostico,
)

__all__ = [
    "get_coevolucion_nacional",
    "get_distribucion_regional",
    "get_mapa_colombia",
    "get_top_areas_conocimiento",
    "get_modelo_estadistico",
    "get_resource_types_diagnostico",
]
