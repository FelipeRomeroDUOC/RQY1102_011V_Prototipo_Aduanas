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
    conn.close()

    if not user:
        return False
    if not verify_password(password, user['password_hash']):
        return False
    return user
