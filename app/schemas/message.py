from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class MessageBase(BaseModel):
    session_id: str
    content: str
    sender: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    message_id: str
    timestamp: datetime
    meta_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class MessageFilter(BaseModel):
    session_id: str
    sender: Optional[str] = None
    limit: int = 10
    offset: int = 0
