from fastapi import APIRouter, Depends, Query, status
from pdi.schemas import CruceCreate, CruceResponse, ViajeroDetailResponse, ViajeroCreate, HistorialCrucesResponse
from pdi.service import create_cruce, get_viajero_by_rut, get_historial_cruces, create_viajero
from auth.dependencies import require_roles
from fastapi import HTTPException

router = APIRouter(prefix="/pdi", tags=["pdi"])

@router.post("/cruces", response_model=CruceResponse, status_code=status.HTTP_201_CREATED)
def registrar_cruce(cruce: CruceCreate, current_user: dict = Depends(require_roles(["FUNCIONARIO_PDI"]))):
    return create_cruce(cruce, current_user["user_id"])

@router.get("/viajeros/{rut_pasaporte}", response_model=ViajeroDetailResponse)
def obtener_viajero(rut_pasaporte: str, current_user: dict = Depends(require_roles(["FUNCIONARIO_PDI"]))):
    viajero = get_viajero_by_rut(rut_pasaporte)
    if not viajero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viajero no encontrado")
    return viajero

@router.get("/cruces/{rut_pasaporte}/historial", response_model=HistorialCrucesResponse)
def obtener_historial(
    rut_pasaporte: str, 
    limite: int = Query(20), 
    tipo: str = Query("TODOS"),
    current_user: dict = Depends(require_roles(["FUNCIONARIO_PDI"]))
):
    return get_historial_cruces(rut_pasaporte, limite, tipo)

@router.post("/viajeros", status_code=status.HTTP_201_CREATED)
def registrar_viajero(viajero: ViajeroCreate, current_user: dict = Depends(require_roles(["FUNCIONARIO_PDI"]))):
    v = create_viajero(viajero)
    return v
