from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageFilter
from typing import List, Optional
import uuid
from datetime import datetime

class MessageRepository:
    def __init__(self, db: Session):
        """Inicializa el repositorio con una sesión activa de base de datos."""
        self.db = db

    def create(self, message: MessageCreate, metadata: dict = None) -> Message:
        """
        Crea y guarda un nuevo mensaje en la base de datos.
        Genera automáticamente el message_id (UUID) y el timestamp.
        Retorna el objeto Message ya guardado con su ID asignado.
        """
        db_message = Message(
            message_id=str(uuid.uuid4()),
            session_id=message.session_id,
            content=message.content,
            sender=message.sender,
            timestamp=datetime.utcnow(),
            meta_data=metadata
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_by_session_id(self, session_id: str, limit: int = 10, offset: int = 0, sender: Optional[str] = None) -> List[Message]:
        """
        Consulta los mensajes de una sesión en la base de datos.
        Permite filtrar por remitente (sender) y aplicar paginación (limit/offset).
        Retorna una lista de mensajes que coincidan con los criterios.
        """
        query = self.db.query(Message).filter(Message.session_id == session_id)

        if sender:
            query = query.filter(Message.sender == sender)

        return query.offset(offset).limit(limit).all()
