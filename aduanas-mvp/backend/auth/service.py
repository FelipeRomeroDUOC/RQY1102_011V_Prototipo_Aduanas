import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import sqlite3
from database import DB_PATH

SECRET_KEY = "aduanas_super_secret_key_mvp"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 8 * 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(rut: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE rut = ? AND activo = 1", (rut,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return {"error": "Credenciales inválidas"}
        
    # Verificar si está bloqueado
    if user['bloqueado_hasta']:
        bloqueado_hasta = datetime.fromisoformat(user['bloqueado_hasta'])
        if datetime.utcnow() < bloqueado_hasta:
            conn.close()
            return {"error": "La cuenta está bloqueada. Intente más tarde."}
        else:
            # Desbloquear si ya pasó el tiempo
            cursor.execute("UPDATE usuarios SET intentos_fallidos = 0, bloqueado_hasta = NULL WHERE id = ?", (user['id'],))
            conn.commit()

    if not verify_password(password, user['password_hash']):
        intentos = user['intentos_fallidos'] + 1
        if intentos >= 5:
            # Bloquear por 15 minutos
            bloqueado_hasta = (datetime.utcnow() + timedelta(minutes=15)).isoformat()
            cursor.execute("UPDATE usuarios SET intentos_fallidos = ?, bloqueado_hasta = ? WHERE id = ?", (intentos, bloqueado_hasta, user['id']))
            conn.commit()
            conn.close()
            return {"error": "Demasiados intentos fallidos. La cuenta ha sido bloqueada."}
        else:
            cursor.execute("UPDATE usuarios SET intentos_fallidos = ? WHERE id = ?", (intentos, user['id']))
            conn.commit()
            conn.close()
            return {"error": "Credenciales inválidas"}
            
    # Reset de intentos al tener login exitoso
    if user['intentos_fallidos'] > 0:
        cursor.execute("UPDATE usuarios SET intentos_fallidos = 0, bloqueado_hasta = NULL WHERE id = ?", (user['id'],))
        conn.commit()
        
    user_dict = dict(user)
    conn.close()
    return user_dict
