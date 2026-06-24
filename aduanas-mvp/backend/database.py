import sqlite3
import os

DB_PATH = "aduanas.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        rut         TEXT    NOT NULL UNIQUE,
        nombre      TEXT    NOT NULL,
        apellido    TEXT    NOT NULL,
        password_hash TEXT  NOT NULL,
        rol         TEXT    NOT NULL CHECK(rol IN ('FUNCIONARIO_PDI', 'FUNCIONARIO_SAG', 'FUNCIONARIO_ADUANAS', 'ADMINISTRADOR')),
        activo      INTEGER NOT NULL DEFAULT 1,
        intentos_fallidos INTEGER NOT NULL DEFAULT 0,
        bloqueado_hasta TEXT,
        creado_en   TEXT    NOT NULL DEFAULT (datetime('now'))
    );
    ''')

    # Viajeros
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS viajeros (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        rut_pasaporte   TEXT    NOT NULL UNIQUE,
        nombre          TEXT    NOT NULL,
        apellido        TEXT    NOT NULL,
        nacionalidad    TEXT    NOT NULL,
        fecha_nacimiento TEXT   NOT NULL,
        tipo_documento  TEXT    NOT NULL CHECK(tipo_documento IN ('RUT', 'PASAPORTE', 'DNI')),
        creado_en       TEXT    NOT NULL DEFAULT (datetime('now'))
    );
    ''')

    # Cruces
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cruces (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        viajero_id          INTEGER NOT NULL REFERENCES viajeros(id),
        tipo                TEXT    NOT NULL CHECK(tipo IN ('INGRESO', 'EGRESO')),
        fecha_hora          TEXT    NOT NULL DEFAULT (datetime('now')),
        funcionario_pdi_id  INTEGER NOT NULL REFERENCES usuarios(id),
        estado_documentos   TEXT    NOT NULL CHECK(estado_documentos IN ('VALIDO', 'OBSERVADO', 'RECHAZADO')),
        observaciones       TEXT,
        creado_en           TEXT    NOT NULL DEFAULT (datetime('now'))
    );
    ''')

    # Vehículos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehiculos (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        patente     TEXT    NOT NULL UNIQUE,
        tipo        TEXT    NOT NULL CHECK(tipo IN ('AUTO', 'CAMIONETA', 'MOTO', 'BUS', 'CAMION')),
        marca       TEXT    NOT NULL,
        modelo      TEXT    NOT NULL,
        anio        INTEGER NOT NULL,
        pais_origen TEXT    NOT NULL DEFAULT 'CL',
        tipo_placa  TEXT    NOT NULL DEFAULT 'PARTICULAR' CHECK(tipo_placa IN ('PARTICULAR', 'DIPLOMATICA')),
        creado_en   TEXT    NOT NULL DEFAULT (datetime('now'))
    );
    ''')

    # Salidas temporales
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS salidas_temporales (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        vehiculo_id             INTEGER NOT NULL REFERENCES vehiculos(id),
        viajero_id              INTEGER NOT NULL REFERENCES viajeros(id),
        funcionario_id          INTEGER NOT NULL REFERENCES usuarios(id),
        fecha_salida            TEXT    NOT NULL DEFAULT (datetime('now')),
        fecha_retorno_estimada  TEXT    NOT NULL,
        estado_documentos       TEXT    NOT NULL CHECK(estado_documentos IN ('VALIDO', 'OBSERVADO', 'RECHAZADO')),
        observaciones           TEXT,
        creado_en               TEXT    NOT NULL DEFAULT (datetime('now'))
    );
    ''')

    # Declaraciones SAG
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS declaraciones_sag (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        viajero_id          INTEGER NOT NULL REFERENCES viajeros(id),
        cruce_id            INTEGER REFERENCES cruces(id),
        funcionario_sag_id  INTEGER NOT NULL REFERENCES usuarios(id),
        productos_declarados TEXT   NOT NULL,  -- JSON array de strings
        incluye_mascotas    INTEGER NOT NULL DEFAULT 0,
        resultado           TEXT    CHECK(resultado IN ('APROBADO', 'RETENIDO', 'DECOMISADO', 'PENDIENTE')) DEFAULT 'PENDIENTE',
        observaciones       TEXT,
        fecha               TEXT    NOT NULL DEFAULT (datetime('now')),
        creado_en           TEXT    NOT NULL DEFAULT (datetime('now'))
    );
    ''')

    conn.commit()
    conn.close()
