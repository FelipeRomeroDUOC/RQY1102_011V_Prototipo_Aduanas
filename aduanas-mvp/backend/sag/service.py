import sqlite3
import json
from database import DB_PATH
from fastapi import HTTPException, status
from sag.schemas import DeclaracionCreate, ResultadoUpdate
from datetime import datetime

def create_declaracion(declaracion: DeclaracionCreate, user_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM viajeros WHERE rut_pasaporte = ?", (declaracion.rut_pasaporte,))
    viajero = cursor.fetchone()
    if not viajero:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Viajero no encontrado")
        
    # Regla de negocio: mayor de 18 años. Anotar en observaciones si es menor.
    obs = declaracion.observaciones or ""
    try:
        nacimiento = datetime.strptime(viajero["fecha_nacimiento"], "%Y-%m-%d")
        edad = (datetime.now() - nacimiento).days // 365
        if edad < 18:
            obs = f"[MENOR DE EDAD ({edad} años)] {obs}"
    except ValueError:
        pass # Ignorar si la fecha tiene otro formato
        
    productos_json = json.dumps(declaracion.productos_declarados)
    
    cursor.execute("""
        INSERT INTO declaraciones_sag (viajero_id, cruce_id, funcionario_sag_id, productos_declarados, incluye_mascotas, observaciones)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (viajero["id"], declaracion.cruce_id, user_id, productos_json, 1 if declaracion.incluye_mascotas else 0, obs))
    dec_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM declaraciones_sag WHERE id = ?", (dec_id,))
    dec = cursor.fetchone()
    conn.close()
    
    return {
        "id": dec["id"],
        "viajero": f"{viajero['nombre']} {viajero['apellido']}",
        "productos_declarados": json.loads(dec["productos_declarados"]),
        "incluye_mascotas": bool(dec["incluye_mascotas"]),
        "resultado": dec["resultado"],
        "fecha": dec["fecha"]
    }

def update_resultado(dec_id: int, resultado_data: ResultadoUpdate):
    if resultado_data.resultado not in ('APROBADO', 'RETENIDO', 'DECOMISADO', 'PENDIENTE'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resultado no válido")
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM declaraciones_sag WHERE id = ?", (dec_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Declaración no encontrada")
        
    cursor.execute("""
        UPDATE declaraciones_sag 
        SET resultado = ?, observaciones = observaciones || '\n' || ?
        WHERE id = ?
    """, (resultado_data.resultado, resultado_data.observaciones or "", dec_id))
    
    conn.commit()
    conn.close()
    return {"detail": "Declaración actualizada con el resultado"}

def get_productos_permitidos():
    return {
        "permitidos": [
            { "categoria": "Lácteos procesados", "ejemplos": ["queso envasado", "mantequilla"] },
            { "categoria": "Carnes cocidas envasadas", "ejemplos": ["jamón envasado"] },
            { "categoria": "Alimentos no perecibles", "ejemplos": ["conservas", "pastas secas"] },
            { "categoria": "Animales / Mascotas", "ejemplos": ["perros", "gatos"] }
        ],
        "no_permitidos": [
            { "categoria": "Frutas y verduras frescas", "ejemplos": ["manzanas", "tomates"] },
            { "categoria": "Carnes frescas o refrigeradas", "ejemplos": ["carne cruda", "embutidos frescos"] },
            { "categoria": "Plantas y semillas", "ejemplos": ["esquejes", "semillas sin certificado"] }
        ]
    }
