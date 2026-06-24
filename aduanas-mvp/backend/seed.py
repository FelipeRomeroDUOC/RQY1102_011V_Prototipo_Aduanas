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

    # Viajero de prueba
    cursor.execute("SELECT COUNT(*) FROM viajeros WHERE rut_pasaporte = '12345678-9'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO viajeros (rut_pasaporte, nombre, apellido, nacionalidad, fecha_nacimiento, tipo_documento)
            VALUES ('12345678-9', 'María', 'González', 'Chilena', '1990-05-15', 'RUT')
        """)
        conn.commit()
        print("Viajero de prueba creado.")

    # Vehículo de prueba
    cursor.execute("SELECT COUNT(*) FROM vehiculos WHERE patente = 'ABCD12'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO vehiculos (patente, tipo, marca, modelo, anio, tipo_placa)
            VALUES ('ABCD12', 'CAMIONETA', 'Toyota', 'Hilux', 2022, 'PARTICULAR')
        """)
        conn.commit()
        print("Vehículo de prueba creado.")

    conn.close()

if __name__ == "__main__":
    seed_db()
