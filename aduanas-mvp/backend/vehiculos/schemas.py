from pydantic import BaseModel
from typing import Optional

class VehiculoCreate(BaseModel):
    patente: str
    tipo: str
    marca: str
    modelo: str
    anio: int
    pais_origen: str = "CL"
    tipo_placa: str = "PARTICULAR"

class VehiculoResponse(VehiculoCreate):
    id: int

class SalidaTemporalCreate(BaseModel):
    patente: str
    rut_pasaporte_conductor: str
    fecha_retorno_estimada: str
    estado_documentos: str
    observaciones: Optional[str] = ""

class VehiculoBasico(BaseModel):
    patente: str
    marca: str
    modelo: str
    anio: int

class SalidaTemporalResponse(BaseModel):
    id: int
    vehiculo: VehiculoBasico
    conductor: str
    fecha_salida: str
    fecha_retorno_estimada: str
    estado_documentos: str

class UltimaSalidaTemporal(BaseModel):
    id: int
    fecha_salida: str
    fecha_retorno_estimada: str
    estado_documentos: str

class VehiculoDetailResponse(BaseModel):
    patente: str
    tipo: str
    marca: str
    modelo: str
    anio: int
    pais_origen: str
    tipo_placa: str
    ultima_salida_temporal: Optional[UltimaSalidaTemporal] = None
