from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageFilter
from typing import List, Optional
import uuid
from datetime import datetime

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, message: MessageCreate, metadata: dict = None) -> Message:
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
        query = self.db.query(Message).filter(Message.session_id == session_id)
        
        if sender:
            query = query.filter(Message.sender == sender)
            
        return query.offset(offset).limit(limit).all()
