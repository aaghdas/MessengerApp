
# Hier werden die Sicherheitsfunktionen für: Passwort hashen, Passwort prüfen, JWT Access Token erstellen, definiert.
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.config import settings
import secrets 
# für die Generierung von sicheren Reset-Codes.secrets ist für sicherheitsrelevante Zufallswerte besser geeignet als random.


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


# Prüft ein JWT Access Token und gibt die Benutzer-ID zurück.
# Bei ungültigem, abgelaufenem oder fehlerhaftem Token wird None zurückgegeben.
def decode_access_token(token: str) -> int | None:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except (JWTError, ValueError):
        return None

# Erstellt einen zufälligen numerischen Reset-Code.
# Der Code wird aktuell für den Passwort-Reset in der Entwicklungs-/Abgabeversion genutzt.
# Später kann die Zustellung über einen sicheren Kanal ergänzt werden.
def create_password_reset_code() -> str:
    return str(secrets.randbelow(900000) + 100000)