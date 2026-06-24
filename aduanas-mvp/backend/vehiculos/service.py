import sqlite3
from database import DB_PATH
from fastapi import HTTPException, status
from vehiculos.schemas import VehiculoCreate, SalidaTemporalCreate
from datetime import datetime

def create_vehiculo(vehiculo_data: VehiculoCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vehiculos (patente, tipo, marca, modelo, anio, pais_origen, tipo_placa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (vehiculo_data.patente, vehiculo_data.tipo, vehiculo_data.marca, vehiculo_data.modelo, vehiculo_data.anio, vehiculo_data.pais_origen, vehiculo_data.tipo_placa))
        vehiculo_id = cursor.lastrowid
        conn.commit()
        
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehiculos WHERE id = ?", (vehiculo_id,))
        v = cursor.fetchone()
        return dict(v)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Patente ya registrada")
    finally:
        conn.close()

def get_vehiculo_by_patente(patente: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM vehiculos WHERE patente = ?", (patente,))
    vehiculo = cursor.fetchone()
    if not vehiculo:
        conn.close()
        return None
        
    cursor.execute("SELECT * FROM salidas_temporales WHERE vehiculo_id = ? ORDER BY fecha_salida DESC LIMIT 1", (vehiculo["id"],))
    ultima_salida = cursor.fetchone()
    conn.close()
    
    vehiculo_dict = dict(vehiculo)
    vehiculo_dict["ultima_salida_temporal"] = dict(ultima_salida) if ultima_salida else None
    return vehiculo_dict

def create_salida_temporal(salida_data: SalidaTemporalCreate, user_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM vehiculos WHERE patente = ?", (salida_data.patente,))
    vehiculo = cursor.fetchone()
    if not vehiculo:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehículo no encontrado")
        
    cursor.execute("SELECT * FROM viajeros WHERE rut_pasaporte = ?", (salida_data.rut_pasaporte_conductor,))
    conductor = cursor.fetchone()
    if not conductor:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conductor no encontrado. Por favor, registre al conductor primero.")
        
    # Validar regla de negocio de días (180 días normal, 90 diplomático)
    try:
        fecha_retorno = datetime.strptime(salida_data.fecha_retorno_estimada, "%Y-%m-%d").date()
        fecha_salida_dt = datetime.now().date()
        dias_estimados = (fecha_retorno - fecha_salida_dt).days
        
        max_dias = 90 if vehiculo["tipo_placa"] == "DIPLOMATICA" else 180
        
        if dias_estimados > max_dias:
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"El plazo máximo de salida temporal es {max_dias} días corridos."
            )
    except ValueError:
        pass # Ignorar formato inválido
        
    cursor.execute("""
        INSERT INTO salidas_temporales (vehiculo_id, viajero_id, funcionario_id, fecha_retorno_estimada, estado_documentos, observaciones)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (vehiculo["id"], conductor["id"], user_id, salida_data.fecha_retorno_estimada, salida_data.estado_documentos, salida_data.observaciones))
    
    salida_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM salidas_temporales WHERE id = ?", (salida_id,))
    salida = cursor.fetchone()
    conn.close()
    
    return {
        "id": salida["id"],
        "vehiculo": {
            "patente": vehiculo["patente"],
            "marca": vehiculo["marca"],
            "modelo": vehiculo["modelo"],
            "anio": vehiculo["anio"]
        },
        "conductor": f"{conductor['nombre']} {conductor['apellido']}",
        "fecha_salida": salida["fecha_salida"],
        "fecha_retorno_estimada": salida["fecha_retorno_estimada"],
        "estado_documentos": salida["estado_documentos"]
    }
