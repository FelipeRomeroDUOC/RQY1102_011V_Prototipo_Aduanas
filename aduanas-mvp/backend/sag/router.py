from fastapi import APIRouter, Depends, status
from sag.schemas import DeclaracionCreate, DeclaracionResponse, ResultadoUpdate
from sag.service import create_declaracion, update_resultado, get_productos_permitidos
from auth.dependencies import require_roles

router = APIRouter(prefix="/sag", tags=["sag"])

@router.post("/declaraciones", response_model=DeclaracionResponse, status_code=status.HTTP_201_CREATED)
def registrar_declaracion(declaracion: DeclaracionCreate, current_user: dict = Depends(require_roles(["FUNCIONARIO_SAG"]))):
    return create_declaracion(declaracion, current_user["user_id"])

@router.patch("/declaraciones/{id}/resultado")
def cambiar_resultado(id: int, resultado: ResultadoUpdate, current_user: dict = Depends(require_roles(["FUNCIONARIO_SAG"]))):
    return update_resultado(id, resultado)

@router.get("/productos-permitidos")
def listar_productos_permitidos(current_user: dict = Depends(require_roles(["FUNCIONARIO_SAG"]))):
    return get_productos_permitidos()
