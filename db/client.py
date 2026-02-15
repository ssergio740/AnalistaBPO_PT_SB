
import config as config
from pymongo import AsyncMongoClient


database= config.settings.MONGO_URI
cliente = AsyncMongoClient(database)

db=cliente[config.settings.MONGO_DB_NAME]

Empresas_db = db[config.settings.MONGO_EMPRESAS]
Casos_db = db[config.settings.MONGO_CASOS]

async def check_db():
    try:
        await cliente.admin.command('ping')
        return "Conexión a MongoDB exitosa"
    except Exception as e:
        return f"Error en DB: {e}"