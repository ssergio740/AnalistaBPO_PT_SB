from pydantic_settings import BaseSettings, SettingsConfigDict
import os
class Settings(BaseSettings):
    # Definir la variable y su tipo
    GOOGLE_API_KEY: str 
    MONGO_DB_NAME:str
    MONGO_URI: str
    MONGO_EMPRESAS: str
    MONGO_CASOS: str

    # Configuración para leer el archivo .env
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), ".env"), extra="ignore",env_file_encoding="utf-8")

# Instancia única (Singleton)
settings = Settings()