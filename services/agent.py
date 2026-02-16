import os
import json
from config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from services.tools.solicitud import guardar_caso_tool
from db.models.solcitud import EmpresaConfig

os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

# Modelo configurado
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

def _crear_prompt_template(empresa: EmpresaConfig) -> str:
    """
    Crea el prompt del sistema para el agente especializado.
    """
    prompt = f"""Eres un agente especializado en procesar solicitudes para la empresa {empresa.compania}.

Categorías válidas: {', '.join(empresa.categorias)}

Reglas de priorización:
{empresa.reglas_prioridad}

Asignaciones de delegación por categoría:
{chr(10).join([f"- {cat}: {email}" for cat, email in empresa.delegaciones.items()])}

Servicio externo:
- Requiere servicio externo: {empresa.servicio_prioridad_externo.requiere_externo}
- URL: {empresa.servicio_prioridad_externo.url if empresa.servicio_prioridad_externo.url else 'N/A'}

Tu tarea:
1. Analiza la solicitud recibida
2. Determina la categoría que mejor la describe
3. Asigna el nivel de prioridad según las reglas
4. Identifica si requiere delegación o servicio externo
5. Proporciona una respuesta clara al cliente

IMPORTANTE: Responde SIEMPRE en formato JSON válido con estos campos exactos:
{{
    "categoria": "nombre de la categoría",
    "prioridad": "alta/media/baja",
    "respuesta": "tu respuesta al cliente",
    "delegacion_email": "email si aplica o null",
    "requiere_externo": true/false
}}"""
    return prompt

async def procesar_solicitud(empresa: EmpresaConfig, solicitud_id: str, descripcion: str) -> dict:
    """
    Procesa una solicitud usando el LLM con instrucciones claras.
    
    Args:
        empresa: Configuración de la empresa
        solicitud_id: ID de la solicitud
        descripcion: Descripción de la solicitud
        
    Returns:
        dict: Resultado del procesamiento
    """
    try:
        # Crear el prompt completo
        system_prompt = _crear_prompt_template(empresa)
        
        user_prompt = f"""Procesa esta solicitud:

ID: {solicitud_id}
Descripción: {descripcion}

Responde en formato JSON válido."""
        
        # Combinar prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        # Invocar el LLM directamente con string
        response = llm.invoke(full_prompt)
        response_text = response.content
        
        # Extraer y parsear JSON de la respuesta
        try:
            # Buscar JSON en la respuesta
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            
            if start == -1 or end <= start:
                # Si no hay JSON, retornar respuesta como está
                return {
                    "output": {"respuesta": response_text},
                    "status": "success"
                }
            
            json_str = response_text[start:end]
            resultado_json = json.loads(json_str)
            
            # Guardar el caso en la BD
            try:
                await guardar_caso_tool(
                    solicitud_id=solicitud_id,
                    compania=empresa.compania,
                    respuesta=resultado_json.get("respuesta", "Procesada"),
                    categoria=resultado_json.get("categoria", "general"),
                    prioridad=resultado_json.get("prioridad", "media")
                )
            except Exception as save_error:
                print(f"Error guardando caso: {save_error}")
            
            return {
                "output": resultado_json,
                "status": "success"
            }
            
        except json.JSONDecodeError as e:
            # Si falla el parsing, retornar la respuesta como texto
            return {
                "output": {"respuesta": response_text},
                "status": "success"
            }
        
    except Exception as e:
        return {
            "error": str(e),
            "output": None,
            "status": "error"
        }