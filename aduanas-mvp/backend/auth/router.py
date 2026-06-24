from fastapi import APIRouter, HTTPException, status
from auth.schemas import LoginRequest, LoginResponse, Usuario
from auth.service import authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    user = authenticate_user(request.rut, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    token_data = {
        "sub": user["rut"],
        "rol": user["rol"],
        "nombre": f"{user['nombre']} {user['apellido']}",
        "user_id": user["id"]
    }
    token = create_access_token(token_data)
    
    usuario_resp = Usuario(
        id=user["id"],
        rut=user["rut"],
        nombre=user["nombre"],
        apellido=user["apellido"],
        rol=user["rol"]
    )
    
    return LoginResponse(token=token, usuario=usuario_resp)

@router.post("/logout")
def logout():
    # El logout real ocurre en el cliente eliminando el token.
    return {"detail": "Logout exitoso"}
