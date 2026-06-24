from fastapi import APIRouter, Depends, status, HTTPException
from vehiculos.schemas import VehiculoCreate, VehiculoResponse, VehiculoDetailResponse, SalidaTemporalCreate, SalidaTemporalResponse
from vehiculos.service import create_vehiculo, get_vehiculo_by_patente, create_salida_temporal
from auth.dependencies import require_roles

router = APIRouter(prefix="/vehiculos", tags=["vehiculos"])

@router.post("", response_model=VehiculoResponse, status_code=status.HTTP_201_CREATED)
def registrar_vehiculo(vehiculo: VehiculoCreate, current_user: dict = Depends(require_roles(["FUNCIONARIO_ADUANAS"]))):
    return create_vehiculo(vehiculo)

@router.get("/{patente}", response_model=VehiculoDetailResponse)
def consultar_vehiculo(patente: str, current_user: dict = Depends(require_roles(["FUNCIONARIO_ADUANAS"]))):
    vehiculo = get_vehiculo_by_patente(patente)
    if not vehiculo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehículo no encontrado")
    return vehiculo

@router.post("/salidas-temporales", response_model=SalidaTemporalResponse, status_code=status.HTTP_201_CREATED)
def registrar_salida_temporal(salida: SalidaTemporalCreate, current_user: dict = Depends(require_roles(["FUNCIONARIO_ADUANAS"]))):
    return create_salida_temporal(salida, current_user["user_id"])
