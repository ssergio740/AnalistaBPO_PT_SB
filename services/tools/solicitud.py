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

@tool("buscar_casos_similares")
async def buscar_casos_similares_tool(compania: str, descripcion: str, limite: int = 3) -> str:
    """
    Busca casos históricos similares de la empresa para contexto.
    
    Args:
        compania: Nombre de la empresa
        descripcion: Descripción para buscar similares
        limite: Cantidad máxima de casos a retornar
        
    Returns:
        str: JSON con casos similares encontrados
    """
    try:
        # Búsqueda simple por empresa (en producción usar búsqueda semántica)
        casos = await Casos_db.find({
            "compania": compania
        }).limit(limite).to_list(length=limite)
        
        if not casos:
            return "No hay casos anteriores registrados para esta empresa."
        
        casos_formateados = []
        for caso in casos:
            caso["_id"] = str(caso["_id"])
            casos_formateados.append(caso)
        
        return json.dumps(casos_formateados, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error al buscar casos: {str(e)}"