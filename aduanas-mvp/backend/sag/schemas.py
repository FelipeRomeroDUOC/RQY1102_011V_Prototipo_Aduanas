from pydantic import BaseModel
from typing import List, Optional

class DeclaracionCreate(BaseModel):
    rut_pasaporte: str
    cruce_id: int
    productos_declarados: List[str]
    incluye_mascotas: bool = False
    observaciones: Optional[str] = ""

class DeclaracionResponse(BaseModel):
    id: int
    viajero: str
    productos_declarados: List[str]
    incluye_mascotas: bool
    resultado: str
    fecha: str

class ResultadoUpdate(BaseModel):
    resultado: str # APROBADO, RETENIDO, DECOMISADO, PENDIENTE
    observaciones: Optional[str] = ""
