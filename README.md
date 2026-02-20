# API de Chat - Prueba Técnica Nequi

API RESTful para procesamiento de mensajes de chat, construida con FastAPI y SQLite.

## Requisitos

- Python 3.11+

## Instalación y ejecución

**1. Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd PruebaTecnicaNequi
```

**2. Crear y activar el entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**4. Iniciar el servidor**
```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://127.0.0.1:8000`

Documentación interactiva: `http://127.0.0.1:8000/docs`

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/messages/` | Enviar un mensaje |
| GET | `/api/messages/{session_id}` | Obtener mensajes de una sesión |
| WS | `/ws` | Canal WebSocket en tiempo real |

### Ejemplo POST

```json
{
  "session_id": "sesion-001",
  "content": "Hola mundo",
  "sender": "user"
}
```

### Parámetros GET

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `limit` | int | Cantidad de mensajes (por defecto 10) |
| `offset` | int | Desde qué posición (por defecto 0) |
| `sender` | string | Filtrar por remitente (`user` o `system`) |

## Pruebas

```bash
# Pruebas de los endpoints REST
python verification_script.py

# Prueba del WebSocket (requiere servidor corriendo)
python test_websocket.py
```
