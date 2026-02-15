from fastapi import APIRouter, HTTPException
from db.models.solcitud import Solicitud, EmpresaConfig
from services.agent import procesar_solicitud
from db.client import Empresas_db, Casos_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/procesar-solicitud")
async def procesar(solicitud: Solicitud):
    """
    Endpoint principal para procesar solicitudes.
    
    1. Valida que la empresa exista
    2. Busca contexto de casos anteriores
    3. Ejecuta el agente para procesar la solicitud
    4. Guarda el resultado en base de datos
    5. Retorna la respuesta al cliente
    """
    try:
        # Buscar la configuración de la empresa
        empresa_doc = await Empresas_db.find_one({"compania": solicitud.compania})
        
        if not empresa_doc:
            logger.warning(f"Empresa no encontrada: {solicitud.compania}")
            raise HTTPException(
                status_code=404, 
                detail=f"Empresa '{solicitud.compania}' no encontrada en el sistema"
            )
        
        # Convertir documento MongoDB a modelo Pydantic
        empresa_doc["_id"] = str(empresa_doc["_id"])
        empresa = EmpresaConfig(**empresa_doc)
        
        logger.info(f"Procesando solicitud {solicitud.solicitud_id} para {solicitud.compania}")
        
        duplicate = await Casos_db.find_one({"compania": solicitud.compania, "solicitud_id": solicitud.solicitud_id})
        if duplicate:
            logger.warning(f"Solicitud duplicada: {solicitud.solicitud_id}")
            raise HTTPException(
                status_code=400,
                detail=f"Solicitud con ID '{solicitud.solicitud_id}' de la empresa {solicitud.compania} ya ha sido procesada. Detalles: {duplicate}"
            )
        # Ejecutar el agente para procesar la solicitud
        resultado_agente = await procesar_solicitud(
            empresa=empresa,
            solicitud_id=solicitud.solicitud_id,
            descripcion=solicitud.solicitud_descripcion
        )
        
        if "error" in resultado_agente:
            logger.error(f"Error en el agente: {resultado_agente['error']}")
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar solicitud: {resultado_agente['error']}"
            )
        
        # Guardar la solicitud original y resultado en la BD
        documento_caso = {
            "solicitud_id": solicitud.solicitud_id,
            "compania": solicitud.compania,
            "descripcion_original": solicitud.solicitud_descripcion,
            "resultado_agente": resultado_agente.get("output", {}),
            "pasos_intermedios": resultado_agente.get("intermediate_steps", [])
        }
        
        resultado_bd = await Casos_db.insert_one(documento_caso)
        
        logger.info(f"Solicitud {solicitud.solicitud_id} procesada exitosamente")
        
        return {
            "status": "procesado",
            "solicitud_id": solicitud.solicitud_id,
            "compania": solicitud.compania,
            "respuesta_agente": resultado_agente.get("output", {}),
            "caso_id": str(resultado_bd.inserted_id)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )