import sqlite3
from database import DB_PATH
from fastapi import HTTPException, status
from pdi.schemas import CruceCreate, ViajeroCreate

def get_viajero_by_rut(rut_pasaporte: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM viajeros WHERE rut_pasaporte = ?", (rut_pasaporte,))
    viajero = cursor.fetchone()
    
    if not viajero:
        conn.close()
        return None
        
    cursor.execute("SELECT * FROM cruces WHERE viajero_id = ? ORDER BY fecha_hora DESC LIMIT 1", (viajero["id"],))
    ultimo_cruce = cursor.fetchone()
    conn.close()
    
    viajero_dict = dict(viajero)
    viajero_dict["ultimo_cruce"] = dict(ultimo_cruce) if ultimo_cruce else None
    return viajero_dict

def create_viajero(viajero_data: ViajeroCreate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO viajeros (rut_pasaporte, nombre, apellido, nacionalidad, fecha_nacimiento, tipo_documento)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (viajero_data.rut_pasaporte, viajero_data.nombre, viajero_data.apellido, viajero_data.nacionalidad, viajero_data.fecha_nacimiento, viajero_data.tipo_documento))
        conn.commit()
        return get_viajero_by_rut(viajero_data.rut_pasaporte)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="RUT/Pasaporte ya registrado")
    finally:
        conn.close()

def create_cruce(cruce_data: CruceCreate, user_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM viajeros WHERE rut_pasaporte = ?", (cruce_data.rut_pasaporte,))
    viajero = cursor.fetchone()
    if not viajero:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viajero no encontrado. Por favor, registre al viajero primero.")
    
    # Validar regla de cruce no consecutivo
    cursor.execute("SELECT tipo FROM cruces WHERE viajero_id = ? ORDER BY fecha_hora DESC LIMIT 1", (viajero["id"],))
    ultimo_cruce = cursor.fetchone()
    
    if ultimo_cruce and ultimo_cruce["tipo"] == cruce_data.tipo:
        conn.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El viajero ya tiene un {cruce_data.tipo} registrado sin el movimiento opuesto correspondiente.")
        
    cursor.execute("""
        INSERT INTO cruces (viajero_id, tipo, funcionario_pdi_id, estado_documentos, observaciones)
        VALUES (?, ?, ?, ?, ?)
    """, (viajero["id"], cruce_data.tipo, user_id, cruce_data.estado_documentos, cruce_data.observaciones))
    cruce_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM cruces WHERE id = ?", (cruce_id,))
    cruce = cursor.fetchone()
    conn.close()
    
    return {
        "id": cruce["id"],
        "viajero": {
            "rut_pasaporte": viajero["rut_pasaporte"],
            "nombre": viajero["nombre"],
            "apellido": viajero["apellido"],
            "nacionalidad": viajero["nacionalidad"]
        },
        "tipo": cruce["tipo"],
        "fecha_hora": cruce["fecha_hora"],
        "estado_documentos": cruce["estado_documentos"]
    }

def get_historial_cruces(rut_pasaporte: str, limite: int = 20, tipo: str = "TODOS"):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM viajeros WHERE rut_pasaporte = ?", (rut_pasaporte,))
    viajero = cursor.fetchone()
    if not viajero:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viajero no encontrado")
        
    query = """
        SELECT c.*, u.nombre, u.apellido
        FROM cruces c
        JOIN usuarios u ON c.funcionario_pdi_id = u.id
        WHERE c.viajero_id = ?
    """
    params = [viajero["id"]]
    
    if tipo in ["INGRESO", "EGRESO"]:
        query += " AND c.tipo = ?"
        params.append(tipo)
        
    query += " ORDER BY c.fecha_hora DESC LIMIT ?"
    params.append(limite)
    
    cursor.execute(query, params)
    cruces = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM cruces WHERE viajero_id = ?", (viajero["id"],))
    total = cursor.fetchone()[0]
    
    conn.close()
    
    result_cruces = []
    for c in cruces:
        result_cruces.append({
            "id": c["id"],
            "tipo": c["tipo"],
            "fecha_hora": c["fecha_hora"],
            "estado_documentos": c["estado_documentos"],
            "funcionario": f"{c['nombre']} {c['apellido']}"
        })
        
    return {
        "rut_pasaporte": viajero["rut_pasaporte"],
        "nombre_completo": f"{viajero['nombre']} {viajero['apellido']}",
        "total_cruces": total,
        "cruces": result_cruces
    }
