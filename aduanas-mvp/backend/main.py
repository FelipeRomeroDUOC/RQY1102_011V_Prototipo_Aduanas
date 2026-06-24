from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from seed import seed_db
from auth.router import router as auth_router
from pdi.router import router as pdi_router
from sag.router import router as sag_router
from vehiculos.router import router as vehiculos_router

app = FastAPI(title="Sistema de Aduanas Chile API (MVP)", version="0.3.0-proto.20260624")

# RNF-04: CORS habilitado solo para Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(pdi_router, prefix="/api/v1")
app.include_router(sag_router, prefix="/api/v1")
app.include_router(vehiculos_router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    seed_db()

@app.get("/api/v1/version")
def get_version():
    return {"version": "0.3.0-proto.20260624"}
