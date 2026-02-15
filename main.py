from fastapi import FastAPI
from routers import solicitud
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API de Procesamiento de Solicitudes", version="1.0")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(solicitud.router)