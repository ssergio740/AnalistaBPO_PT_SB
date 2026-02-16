# Sistema de Procesamiento de Solicitudes con Agente IA
**Prueba Técnica - Profesional Senior (Análisis de Datos & IA)**

Seguros Bolívar - Caso de Estudio de Solución de IA

---

## Descripción del Proyecto

Sistema de API REST basado en **FastAPI** que integra un agente de IA (**Google Gemini**) para procesar solicitudes de clientes de forma automática, se escogío Gemini por los créditos disponibles, y su administración de agentes obliga a mantener una buena documentación de las Tools. El sistema:

- Recibe solicitudes en formato estructurado JSON de acuerdo a los basesmodel
- Valida información de la empresa solicitante verificando su existencia
- Procesa solicitudes usando un agente IA
- Categoriza automáticamente según reglas de negocio (Recibidas como JSON)
- Asigna prioridades utilizando el llm
- Guarda resultados en MongoDB
- Implementa validaciones y manejo robusto de errores

---

## Arquitectura

El sistema está organizado en capas modernas:

```
AnalistaBPO_PT_SB/
├── main.py                 # Punto de entrada FastAPI
├── config.py              # Configuración centralizada (variables de entorno)
├── routers/               # Endpoints HTTP
│   └── solicitud.py      # Router principal de procesamiento
├── services/              # Lógica de negocio
│   ├── agent.py          # Orquestación del agente IA
│   └── tools/
│       └── solicitud.py  # Herramientas para el agente
├── db/                    # Acceso a datos
│   ├── client.py         # Conexión MongoDB
│   ├── models/
│   │   └── solicitud.py  # Modelos Pydantic
│   └── schema/
│       └── schemas.py    # Esquemas adicionales
└── requirements.txt       # Dependencias Python
```

Ver `ARQUITECTURA_PROPUESTA.png` para diagrama propuesto para su despliegue en AWS.

---

## Instalación y Configuración

### Requisitos Previos
- **Python 3.9+**
- **MongoDB** (cloud o local)
- **Google API Key** (Google Generative AI)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**
```bash
cd AnalistaBPO_PT_SB
```

2. **Crear archivo de entorno**
```bash
cp .env.example .env
```

3. **Configurar variables de entorno**
Edita `.env` con tus credenciales:
```env
GOOGLE_API_KEY=your_actual_google_api_key
MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=solicitudes_db
MONGO_EMPRESAS=empresas
MONGO_CASOS=casos
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Ejecutar la aplicación**
```bash
fastapi dev main.py
```

La API estará disponible en: `http://localhost:8000`

---

## 📚 Uso de la API

### Endpoint Principal

**POST** `/procesar-solicitud`

**Descripción:** Procesa una solicitud de cliente usando el agente IA

**Request Body:**
```json
{
  "compania": "GASES DEL ORINOCO",
  "solicitud_id": "REQ-001",
  "solicitud_descripcion": "Mi nombre es Juana García, necesito información sobre cobertura de seguros de vida..."
}
```

**Response (Exitoso - 200):**
```json
{
  "status": "procesado",
  "solicitud_id": "REQ-001",
  "compania": "GASES DEL ORINOCO",
  "respuesta_agente": {
    "categoria": "Información de Cobertura",
    "prioridad": "media",
    "respuesta": "Estimada Juana, le informamos que nuestra cobertura de vida...",
    "delegacion_email": "vida@gasesdelorinoco.com",
    "requiere_externo": false
  },
  "caso_id": "507f1f77bcf86cd799439011"
}
```

**Códigos de Error:**
- `404` - Empresa no encontrada
- `400` - Solicitud duplicada o datos inválidos
- `500` - Error interno del servidor

### Ejemplo con cURL
```bash
curl -X POST http://localhost:8000/procesar-solicitud \
  -H "Content-Type: application/json" \
  -d '{
    "compania": "GASES DEL ORINOCO",
    "solicitud_id": "REQ-001",
    "solicitud_descripcion": "Necesito más información sobre mis beneficios"
  }'
```

### Ejemplo con Python
```python
import requests

url = "http://localhost:8000/procesar-solicitud"
payload = {
    "compania": "GASES DEL ORINOCO",
    "solicitud_id": "REQ-101",
    "solicitud_descripcion": "¿Qué documentos necesito para hacer un reclamo?"
}

response = requests.post(url, json=payload)
print(response.json())
```

---

## Configuración de Variables de Entorno

### Archivo `.env`

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | API Key de Google Generative AI | `AIzaSy...` |
| `MONGO_URI` | Conexión a MongoDB | `mongodb+srv://user:pass@cluster.mongodb.net` |
| `MONGO_DB_NAME` | Nombre de la base de datos | `solicitudes_db` |
| `MONGO_EMPRESAS` | Colección de empresas | `empresas` |
| `MONGO_CASOS` | Colección de casos procesados | `casos` |

### Obtener Credenciales

**Google API Key:**
1. Ir a https://console.cloud.google.com
2. Crear un proyecto
3. Habilitar "Google Generative AI API"
4. Crear credenciales (API Key)

**MongoDB Connection String:**
1. Crear cuenta en https://www.mongodb.com/cloud/atlas
2. Crear un cluster
3. Obtener la cadena de conexión
4. Reemplazar placeholders: `<user>`, `<password>`, `<cluster>`

---

## Estructura de Datos

### Colección: `empresas`
```json
{
  "_id": ObjectId,
  "compania": "GASES DEL ORINOCO",
  "categorias": [
    "Información General",
    "Reclamos",
    "Beneficios"
  ],
  "reglas_prioridad": "Reclamos=alta, Gestionarias=media, Informativas=baja",
  "delegaciones": {
    "Información General": "info@empresa.com",
    "Reclamos": "reclamos@empresa.com",
    "Beneficios": "beneficios@empresa.com"
  },
  "servicio_prioridad_externo": {
    "requiere_externo": false,
    "url": null
  }
}
```

### Colección: `casos`
```json
{
  "_id": ObjectId,
  "solicitud_id": "REQ-001",
  "compania": "GASES DEL ORINOCO",
  "descripcion_original": "...",
  "resultado_agente": {
    "categoria": "...",
    "prioridad": "...",
    "respuesta": "...",
    "delegacion_email": "...",
    "requiere_externo": false
  },
  "pasos_intermedios": []
}
```

---

## Testing

Para pruebas interactivas, usa el notebook incluido:
```bash
jupyter notebook pruebas.ipynb
```

O usa la documentación interactiva de FastAPI:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Seguridad

- Validación de entrada con Pydantic
- CORS configurado (solo POST permitido)
- Variables sensibles en archivo `.env`
- Prevención de solicitudes duplicadas
- No incluir `.env` en control de versiones (agregar a `.gitignore`)

---

## Dependencias Principales

| Paquete | Versión | Propósito |
|---------|---------|----------|
| `fastapi` | 0.104.1 | Framework web |
| `uvicorn` | 0.24.0 | Servidor ASGI |
| `pydantic` | 2.5.0 | Validación de datos |
| `pymongo` | 4.6.0 | Driver MongoDB sync |
| `motor` | 3.3.2 | Driver MongoDB async |
| `langchain` | 0.1.0 | Orquestación de IA |
| `google-generativeai` | 0.3.0 | API Gemini |

Ver `requirements.txt` para versiones exactas.

---

## Troubleshooting

**Error: "Empresa no encontrada"**
- Verifica que la empresa exista en la colección `empresas` de MongoDB
- Asegúrate que el nombre sea exacto (diferencia de mayúsculas/minúsculas)

**Error: "Conexión a MongoDB fallida"**
- Valida el `MONGO_URI` en tu `.env`
- Comprueba que el cluster de MongoDB esté activo
- Verifica que tu IP esté en la whitelist de MongoDB Atlas

**Error: "API Key inválida"**
- Genera una nueva API Key en Google Cloud Console
- Asegúrate que la API "Google Generative AI" esté habilitada

**Request sin respuesta**
- Aumenta el timeout del cliente
- Verifica que Gemini responda en formato JSON válido
- Revisa los logs en la consola

---

## Soporte

Para problemas o preguntas, revisa:
- Logs de la aplicación en consola
- Documentación de FastAPI: https://fastapi.tiangolo.com
- Documentación de Gemini: https://ai.google.dev/docs


