from pydantic import BaseModel

class LoginRequest(BaseModel):
    nombre_usuario: str
    contrasena: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
