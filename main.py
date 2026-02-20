from fastapi import FastAPI
from app.api.endpoints import messages, websockets, auth
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.models import message, usuario  # noqa: asegura que ambos modelos se registren

Base.metadata.create_all(bind=engine)

# Crear usuario por defecto al iniciar
from app.services.auth_service import crear_usuario_por_defecto
db = SessionLocal()
crear_usuario_por_defecto(db)
db.close()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(messages.router, prefix="/api/messages", tags=["Mensaje"])
app.include_router(websockets.router, tags=["websockets"])
