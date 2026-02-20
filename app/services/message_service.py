from sqlalchemy.orm import Session
from app.repositories.message_repository import MessageRepository
from app.schemas.message import MessageCreate, MessageResponse
import re

class MessageService:
    def __init__(self, db: Session):
        """Inicializa el servicio con una sesión de base de datos."""
        self.repository = MessageRepository(db)

    def process_message(self, message_in: MessageCreate) -> MessageResponse:
        """
        Procesa un mensaje antes de guardarlo.
        Pasos: filtra malas palabras, calcula metadatos (longitud y conteo de palabras)
        y delega el guardado al repositorio.
        """
        clean_content = self._Filtro_mala_palabras(message_in.content)
        message_in.content = clean_content

        metadata = {
            "Longitud": len(clean_content),
            "Cantidad_palabras": len(clean_content.split())
        }
        return self.repository.create(message_in, metadata)

    def _Filtro_mala_palabras(self, text: str) -> str:
        """
        Reemplaza palabras prohibidas en el texto con '****'.
        Usa expresiones regulares para hacer la búsqueda sin importar mayúsculas/minúsculas.
        """
        malas_palabras = ["therian", "groseria", "insulto"]
        pattern = re.compile(r'\b(' + '|'.join(malas_palabras) + r')\b', re.IGNORECASE)
        return pattern.sub('****', text)

    def get_messages(self, session_id: str, limit: int = 10, offset: int = 0, sender: str = None):
        """
        Obtiene los mensajes de una sesión específica.
        Soporta paginación con limit/offset y filtro opcional por remitente.
        """
        return self.repository.get_by_session_id(session_id, limit, offset, sender)
