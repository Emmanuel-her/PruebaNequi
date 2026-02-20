from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService

router = APIRouter()

def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    return MessageService(db)

@router.post("/", response_model=MessageResponse, status_code=201)
def Crear_mensaje(
    message_in: MessageCreate,
    service: MessageService = Depends(get_message_service)
):
    try:
        return service.process_message(message_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}", response_model=List[MessageResponse])
def Obtener_mensajes(
    session_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    sender: Optional[str] = None,
    service: MessageService = Depends(get_message_service)
):
    messages = service.get_messages(session_id, limit, offset, sender)
    if not messages:
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    return messages
