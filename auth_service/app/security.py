
# Hier werden die Sicherheitsfunktionen für: Passwort hashen, Passwort prüfen, JWT Access Token erstellen, definiert.
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.config import settings


# Passwort-Hashing-Kontext.
# bcrypt wird verwendet, damit echte Passwörter niemals im Klartext gespeichert werden.
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Erstellt einen sicheren Hash aus einem Klartext-Passwort.
def hash_password(password: str) -> str:
    return password_context.hash(password)


# Prüft, ob ein Klartext-Passwort zum gespeicherten Passwort-Hash passt.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


# Erstellt ein JWT Access Token.
# data enthält Informationen, die im Token gespeichert werden sollen,
# z. B. die Benutzer-ID oder E-Mail.
def create_access_token(data: dict) -> str:
    token_data = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token_data.update({"exp": expire})

    encoded_jwt = jwt.encode(
        token_data,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return encoded_jwt