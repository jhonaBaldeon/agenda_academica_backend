from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .apis import (
    curso_api,
    alumno_api,
    seguimiento_api,
    estadistica_api,
    chatbot_api,
    docente_api,
)

app = FastAPI(
    title="Agenda Académica API",
    description="Backend para la Agenda Académica con soporte para chatbot",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(curso_api.router)
app.include_router(alumno_api.router)
app.include_router(seguimiento_api.router)
app.include_router(estadistica_api.router)
app.include_router(chatbot_api.router)
app.include_router(docente_api.router)


@app.get("/")
def root():
    return {"message": "Agenda Académica API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
