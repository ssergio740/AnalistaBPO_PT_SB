from fastapi import FastAPI
from routers import users
from routers import experiencia,puestos
from routers import education,Skills,proyects,lengua,references,gemini
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=None,redoc_url=None,openapi_url=None)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(users.router)