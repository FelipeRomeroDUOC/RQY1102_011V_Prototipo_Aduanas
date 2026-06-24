# Prototipo MVP del Sistema de Aduanas Chile

Este proyecto es una aplicación web funcional (Prototipo MVP) desarrollada para el Sistema de Aduanas Chile, específicamente para los funcionarios del paso fronterizo Chile-Argentina. El sistema cubre el flujo operativo mínimo: autenticación por rol, control migratorio (PDI), control fitosanitario (SAG) y registro de salida temporal de vehículos (Aduanas).

## Estructura del Proyecto

El proyecto se divide en dos componentes principales:
- **Backend**: Desarrollado en Python con FastAPI y SQLite (base de datos local).
- **Frontend**: Desarrollado en React, Vite y Tailwind CSS.

## Requisitos Previos

- **Node.js** (v18 o superior)
- **Python** (v3.11 o superior)

## Instrucciones de Ejecución

Existen dos maneras de levantar el proyecto: mediante Docker (recomendado para evitar problemas de dependencias) o de forma manual (local).

### Opción A: Usando Docker (Recomendado)

Requiere tener **Docker Desktop** instalado y ejecutándose.

1. Abre una terminal en la raíz del proyecto.
2. Ejecuta el comando para construir y levantar ambos contenedores simultáneamente.

   **En Windows (PowerShell / CMD) y Linux / macOS:**
   ```bash
   docker-compose up --build
   ```
3. El frontend estará disponible en `http://localhost:5173` y la API en `http://localhost:8000`.
4. *(Nota: Cualquier cambio en el código se reflejará en vivo gracias a la configuración de volúmenes).*

### Opción B: Instalación Manual (Local)

Si prefieres no usar Docker, puedes levantar los servidores de forma independiente.

#### 1. Levantar el Backend (FastAPI)

Abre una terminal, navega a la carpeta del backend y configura el entorno.

**En Windows (CMD o PowerShell):**
```powershell
cd aduanas-mvp/backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**En Linux / macOS:**
```bash
cd aduanas-mvp/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

El backend se ejecutará en `http://localhost:8000`. Documentación de la API en `http://localhost:8000/docs`.

#### 2. Levantar el Frontend (React)

Abre una segunda terminal y navega a la carpeta del frontend:

```bash
cd aduanas-mvp/frontend
npm install
npm run dev
```
El frontend se ejecutará en `http://localhost:5173`.

## Usuarios de Prueba (Semilla)

Al iniciar el backend por primera vez, se insertan los siguientes usuarios predeterminados (todos con la contraseña especificada, la cual ha sido hasheada en la base de datos):

| Rol | RUT | Contraseña | Nombre |
|---|---|---|---|
| FUNCIONARIO_PDI | `11111111-1` | `pdi123` | Carlos Muñoz |
| FUNCIONARIO_SAG | `22222222-2` | `sag123` | Ana Torres |
| FUNCIONARIO_ADUANAS | `33333333-3` | `aduanas123` | Pedro Rojas |
| ADMINISTRADOR | `44444444-4` | `admin123` | Admin Sistema |

## Endpoints Principales de la API REST

**Autenticación**
- `POST /api/v1/auth/login`: Iniciar sesión (retorna JWT).
- `POST /api/v1/auth/logout`: Cerrar sesión.

**PDI (Migraciones)**
- `POST /api/v1/pdi/viajeros`: Crear un nuevo viajero.
- `GET /api/v1/pdi/viajeros/{rut_pasaporte}`: Verificar viajero.
- `POST /api/v1/pdi/cruces`: Registrar ingreso o egreso.
- `GET /api/v1/pdi/cruces/{rut_pasaporte}/historial`: Historial de cruces.

**SAG (Fitosanitario)**
- `GET /api/v1/sag/productos-permitidos`: Listado estático de productos.
- `POST /api/v1/sag/declaraciones`: Registrar declaración jurada.
- `PATCH /api/v1/sag/declaraciones/{id}/resultado`: Actualizar resultado de inspección.

**Aduanas (Vehículos)**
- `POST /api/v1/vehiculos`: Registrar vehículo.
- `GET /api/v1/vehiculos/{patente}`: Verificar vehículo.
- `POST /api/v1/vehiculos/salidas-temporales`: Registrar salida temporal de un vehículo.

## Reglas de Negocio Implementadas

- **PDI**: Un viajero no puede tener dos cruces del mismo tipo consecutivos (ej. dos ingresos).
- **SAG**: Validación de declaración para menores de 18 años y registro de ingreso de mascotas.
- **Aduanas**: Límite de días en el extranjero según el tipo de placa (Particular: 180 días, Diplomática: 90 días).
