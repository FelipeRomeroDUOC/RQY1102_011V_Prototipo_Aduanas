# Changelog

Este proyecto utiliza Versionado Semántico (SemVer) adaptado para prototipo bajo el formato `0.MINOR.PATCH-proto.YYYYMMDD`.

## [0.2.0-proto.20260624] - 2026-06-24

### Añadido
- **SAG Fitosanitario**: Se añadió la funcionalidad completa para buscar y actualizar el estado de una Declaración Jurada (CP_SAG_2). Esto incluye un nuevo endpoint `GET /api/v1/sag/declaraciones/{id}` en el backend y la vista `ActualizarDeclaracion.jsx` en el frontend.

## [0.1.2-proto.20250623] - 2025-06-23

### Corregido
- **Seguridad / Login**: Se implementó el control de intentos fallidos en el backend. Ahora las cuentas se bloquean por 15 minutos tras 5 intentos fallidos (CP_Auth_2).
- **Frontend / UI**: Se corrigió el archivo `Login.jsx` que mostraba el mensaje genérico "Credenciales inválidas" independientemente del error devuelto por la API (p.ej., cuando la cuenta estaba bloqueada). Ahora extrae el mensaje de error del payload JSON.

---

## [0.1.1-proto.20250623] - 2025-06-23

### Corregido
- **Dependencia `bcrypt`**: Downgrade de `bcrypt` 5.0.0 → 4.1.3 para resolver incompatibilidad con `passlib`. La versión 5.0 de bcrypt cambió su API interna, provocando un `ValueError` durante la verificación de contraseñas al iniciar el servidor (`Application startup failed`).

---

## [0.1.0-proto.20250623] - 2025-06-23

### Añadido
- **Estructura base del proyecto**: Se crearon las carpetas e inicialización del proyecto para `backend` y `frontend`.
- **Base de Datos**: 
  - Archivo de inicialización `database.py` con SQLite y creación de tablas (usuarios, viajeros, cruces, vehículos, salidas temporales y declaraciones SAG).
  - Script `seed.py` para cargar los 4 usuarios semilla (PDI, SAG, Aduanas y Admin) con contraseñas encriptadas usando `bcrypt`.
- **Backend (FastAPI)**:
  - Módulo `auth`: Endpoints de login, generación de tokens JWT (`HS256`, expiración 8 horas) y dependencias de protección por roles.
  - Módulo `pdi`: Endpoints para creación/verificación de viajeros y registro/historial de cruces, incluyendo validación de cruces no consecutivos.
  - Módulo `sag`: Endpoints para productos permitidos, declaración jurada (con manejo de mascotas y validación de menores) y actualización de estados.
  - Módulo `vehiculos`: Endpoints para creación/verificación de vehículos y registro de salidas temporales, incluyendo control de límites de estadía (90 días diplomáticos / 180 días particulares).
- **Frontend (React / Vite / Tailwind)**:
  - Configuración de Tailwind CSS con paleta de colores institucional oficial de Aduanas Chile.
  - Componentes estructurales de UI: `Layout`, `Navbar` responsiva y sistema de `ProtectedRoute` por roles.
  - Contexto global `AuthContext` para almacenar tokens JWT de forma segura en `sessionStorage`.
  - Página `Login`: Autenticación y enrutamiento inteligente basado en rol de usuario.
  - Páginas PDI: Interfaces de `RegistrarCruce` y `VerificarViajero`.
  - Páginas SAG: Interfaz de `RegistrarDeclaracion`.
  - Páginas Aduanas Vehículos: Interfaces de `RegistrarSalidaTemporal` y `VerificarVehiculo`.
