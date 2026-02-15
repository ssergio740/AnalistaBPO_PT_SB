from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
from datetime import datetime


class Solicitud(BaseModel):
    compania: str = Field(
        ..., 
        examples=["GASES DEL ORINOCO"],
        description="Nombre de la empresa a la que va dirigida la solicitud"
    )
    solicitud_id: str = Field(
        ..., 
        examples=["REQ-001"],
        description="Identificador único de la solicitud proporcionado por el canal digital"
    )
    solicitud_descripcion: str = Field(
        ..., 
        min_length=10,
        examples=["Mi nombre es Juana..."],
        description="Texto libre con la descripción del problema o solicitud"
    )

# Alias para compatibilidad
SolicitudInput = Solicitud

class ServicioExternoConfig(BaseModel):
    requiere_externo: bool
    url: Optional[str]

class EmpresaConfig(BaseModel):
    # Usamos alias para que _id de Mongo no cause conflicto con id de Python
    id: Optional[str] = Field(alias="_id", default=None) 
    compania: str
    categorias: List[str]
    reglas_prioridad: str
    delegaciones: Dict[str, str]
    servicio_prioridad_externo: ServicioExternoConfig

    # Configuración para Pydantic v2
    model_config = ConfigDict(populate_by_name=True)

class RespuestaAgente(BaseModel):
    """Respuesta procesada por el agente"""
    solicitud_id: str
    compania: str
    categoria: str
    prioridad: str
    respuesta: str
    delegacion_email: Optional[str] = None
    requiere_externo: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
