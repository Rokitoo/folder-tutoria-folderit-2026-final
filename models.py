"""Modelos de datos: describen qué campos tiene cada elemento y cómo se validan."""
from pydantic import BaseModel, Field


class LibroNuevo(BaseModel):
    titulo: str = Field(min_length=1)
