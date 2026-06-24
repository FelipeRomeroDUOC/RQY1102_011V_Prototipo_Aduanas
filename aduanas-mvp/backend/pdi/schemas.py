from pydantic import BaseModel
from typing import Optional, List

class CruceCreate(BaseModel):
    rut_pasaporte: str
    tipo: str # INGRESO o EGRESO
    estado_documentos: str # VALIDO, OBSERVADO, RECHAZADO
    observaciones: Optional[str] = ""

class ViajeroBase(BaseModel):
    rut_pasaporte: str
    nombre: str
    apellido: str
    nacionalidad: str

class CruceResponse(BaseModel):
    id: int
    viajero: ViajeroBase
    tipo: str
    fecha_hora: str
    estado_documentos: str

class UltimoCruce(BaseModel):
    tipo: str
    fecha_hora: str
    estado_documentos: str

class ViajeroDetailResponse(ViajeroBase):
    id: int
    fecha_nacimiento: str
    tipo_documento: str
    ultimo_cruce: Optional[UltimoCruce] = None

class ViajeroCreate(BaseModel):
    rut_pasaporte: str
    nombre: str
    apellido: str
    nacionalidad: str
    fecha_nacimiento: str
    tipo_documento: str

class CruceHistorialItem(BaseModel):
    id: int
    tipo: str
    fecha_hora: str
    estado_documentos: str
    funcionario: str

class HistorialCrucesResponse(BaseModel):
    rut_pasaporte: str
    nombre_completo: str
    total_cruces: int
    cruces: List[CruceHistorialItem]
