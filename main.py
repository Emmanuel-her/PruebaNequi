from fastapi import FastAPI
from app.api.endpoints import messages, websockets
from app.core.config import settings
from app.core.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(messages.router, prefix="/api/messages", tags=["Mensaje"])
app.include_router(websockets.router, tags=["websockets"])

