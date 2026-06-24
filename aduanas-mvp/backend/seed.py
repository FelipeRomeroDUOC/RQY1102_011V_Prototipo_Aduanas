from database import init_db, get_db, DB_PATH
import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def seed_db():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    count = cursor.fetchone()[0]

    if count == 0:
        usuarios = [
            ("11111111-1", "Carlos", "Muñoz", get_password_hash("pdi123"), "FUNCIONARIO_PDI"),
            ("22222222-2", "Ana", "Torres", get_password_hash("sag123"), "FUNCIONARIO_SAG"),
            ("33333333-3", "Pedro", "Rojas", get_password_hash("aduanas123"), "FUNCIONARIO_ADUANAS"),
            ("44444444-4", "Admin", "Sistema", get_password_hash("admin123"), "ADMINISTRADOR")
        ]
        
        cursor.executemany("""
            INSERT INTO usuarios (rut, nombre, apellido, password_hash, rol) 
            VALUES (?, ?, ?, ?, ?)
        """, usuarios)
        
        conn.commit()
        print("Base de datos inicializada con usuarios semilla.")
    else:
        print("La base de datos ya contiene usuarios.")

    conn.close()

if __name__ == "__main__":
    seed_db()
