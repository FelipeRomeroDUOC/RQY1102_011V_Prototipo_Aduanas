from pydantic import BaseModel

class LoginRequest(BaseModel):
    rut: str
    password: str

class Usuario(BaseModel):
    id: int
    rut: str
    nombre: str
    apellido: str
    rol: str

class LoginResponse(BaseModel):
    token: str
    usuario: Usuario
