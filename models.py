"""Modelos de datos: describen qué campos tiene cada elemento y cómo se validan."""
from pydantic import BaseModel, Field

class LibroNuevo(BaseModel):
    titulo: str = Field(min_length=1)
    isbn: int = Field(gt=0)
    descripcion: str
    anio: int = Field(ge=0)
    numero_copias: int = Field(ge=0)
    activo: bool
