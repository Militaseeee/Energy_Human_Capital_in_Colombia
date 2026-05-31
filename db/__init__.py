# db/__init__.py — expone get_engine directamente desde el paquete
from .connection import get_engine

__all__ = ["get_engine"]
