from langchain.tools import tool
from db.models.solcitud import Solicitud
from db.client import Casos_db
import json

@tool("guardar_caso")
async def guardar_caso_tool(solicitud_id: str, compania: str, respuesta: str, categoria: str, prioridad: str) -> str:
    """
    Guarda el caso procesado en la base de datos.
    
    Args:
        solicitud_id: ID único de la solicitud
        compania: Nombre de la empresa
        respuesta: Respuesta del agente
        categoria: Categoría asignada
        prioridad: Nivel de prioridad
        
    Returns:
        str: ID del documento insertado en MongoDB
    """
    try:
        documento = {
            "solicitud_id": solicitud_id,
            "compania": compania,
            "respuesta": respuesta,
            "categoria": categoria,
            "prioridad": prioridad
        }
        resultado = await Casos_db.insert_one(documento)
        return f"Caso guardado con ID: {str(resultado.inserted_id)}"
    except Exception as e:
        return f"Error al guardar caso: {str(e)}"

