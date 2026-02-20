from fastapi import FastAPI
from app.api.endpoints import messages, websockets, auth
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.models import message, usuario  

Base.metadata.create_all(bind=engine)

from app.services.auth_service import crear_usuario_por_defecto
db = SessionLocal()
crear_usuario_por_defecto(db)
db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
## API de Chat - Prueba Técnica Nequi

Para probar los endpoints protegidos, primero haz login:

1. Haz clic en **Authorize 🔒**
2. Ingresa las siguientes credenciales:
   - **Username:** `user`
   - **Password:** `123456`
3. Clic en **Authorize**
"""
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(messages.router, prefix="/api/messages", tags=["Mensaje"])
app.include_router(websockets.router, tags=["websockets"])
