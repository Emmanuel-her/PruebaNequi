from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.database import get_db

# que pena esto jamas iria aca pero lo tengo aca pero para realizar la prueba en render debo dejarlo
CLAVE_SECRETA = "clave_super_secreta_cambiar_en_produccion"
ALGORITMO = "HS256"
DURACION_TOKEN_MINUTOS = 60

contexto_contrasena = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    """
    Compara una contraseña en texto con su versión hasheada.
    Retorna True si coinciden, False si no.
    """
    return contexto_contrasena.verify(contrasena_plana, contrasena_hash)


def hashear_contrasena(contrasena: str) -> str:
    """
    Convierte una contraseña en texto a un hash usando bcrypt.
    El hash resultante es lo que se guarda en la base de datos.
    """
    return contexto_contrasena.hash(contrasena)


def crear_token(data: dict) -> str:
    """
    Genera un token JWT firmado con la clave secreta.
    El token incluye los datos del usuario y una fecha de expiración.
    """
    datos = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=DURACION_TOKEN_MINUTOS)
    datos.update({"exp": expiracion})
    return jwt.encode(datos, CLAVE_SECRETA, algorithm=ALGORITMO)


def autenticar_usuario(db: Session, nombre_usuario: str, contrasena: str):
    """
    Busca el usuario en la base de datos y verifica su contraseña.
    Retorna el objeto Usuario si las credenciales son correctas, None si no.
    """
    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    if not usuario:
        return None
    if not verificar_contrasena(contrasena, usuario.contrasena_hash):
        return None
    return usuario


def get_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependencia de FastAPI para proteger endpoints.
    Extrae y valida el token JWT del header 'Authorization: Bearer <token>'.
    Si el token es inválido o expiró, lanza un error 401.
    Se usa con Depends() en los endpoints que requieren autenticación.
    """
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado. Token inválido o expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        nombre_usuario: str = payload.get("sub")
        if nombre_usuario is None:
            raise credenciales_invalidas
    except JWTError:
        raise credenciales_invalidas

    usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    if usuario is None:
        raise credenciales_invalidas
    return usuario


def crear_usuario_por_defecto(db: Session):
    """
    Se ejecuta al iniciar la aplicación.
    Verifica si el usuario 'user' existe en la base de datos.
    Si no existe, lo crea con la contraseña '123456' ya hasheada.
    """
    usuario_existente = db.query(Usuario).filter(Usuario.nombre_usuario == "user").first()
    if not usuario_existente:
        usuario_defecto = Usuario(
            nombre_usuario="user",
            contrasena_hash=hashear_contrasena("123456")
        )
        db.add(usuario_defecto)
        db.commit()
        print("Usuario por defecto creado: user / 123456")
