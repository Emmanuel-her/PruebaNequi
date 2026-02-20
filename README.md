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

> Al iniciar, se crea automáticamente el usuario por defecto si no existe en la base de datos.

## Autenticación

Todos los endpoints de mensajes están protegidos con JWT. Para usarlos:

**1. Obtener el token**

```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user&password=123456
```

Respuesta:
```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}
```

**2. Usar el token en cada petición**

Agrega el token en el header de autorización:
```
Authorization: Bearer <token>
```

**En Swagger UI (`/docs`):**
1. Haz clic en el botón **Authorize 🔒**
2. Ingresa `user` y `123456`
3. Clic en **Authorize** — todos los endpoints quedan desbloqueados

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/auth/login` | ❌ | Obtener token de acceso |
| POST | `/api/messages/` | ✅ | Enviar un mensaje |
| GET | `/api/messages/{session_id}` | ✅ | Obtener mensajes de una sesión |
| WS | `/ws` | ❌ | Canal WebSocket en tiempo real |

### Ejemplo POST /api/messages/

```json
{
  "session_id": "sesion-001",
  "content": "Hola mundo",
  "sender": "user"
}
```

### Parámetros GET /api/messages/{session_id}

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

