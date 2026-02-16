from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
from datetime import datetime


class Solicitud(BaseModel):

    """Es el formato con el que se solicitó recibir la información"""
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


SolicitudInput = Solicitud

class ServicioExternoConfig(BaseModel):
    """Es la configuración para poderse comunicar con servicios externos de acuerdo como lo requiera la empresa"""

    requiere_externo: bool
    url: Optional[str]

class EmpresaConfig(BaseModel):
    """ Represemta la información que se encuentra en la base de datos en MongoDB y que contiene las reglas por negocio"""
    id: Optional[str] = Field(alias="_id", default=None) 
    compania: str
    categorias: List[str]
    reglas_prioridad: str
    delegaciones: Dict[str, str]
    servicio_prioridad_externo: ServicioExternoConfig

    
    model_config = ConfigDict(populate_by_name=True)

class RespuestaAgente(BaseModel):
    """Respuesta procesada por el agente, es lo que se responderá al cliente después de procesar la solicitud."""
    solicitud_id: str
    compania: str
    categoria: str
    prioridad: str
    respuesta: str
    delegacion_email: Optional[str] = None
    requiere_externo: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
