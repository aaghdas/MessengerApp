"""
- Token aus Authorization Header lesen
- Token über shared/auth/jwt.py prüfen
- auth_user_id aus dem Token zurückgeben
"""
# Dependencies für den Messaging Service.
#
# Diese Datei enthält wiederverwendbare FastAPI-Dependencies.
# Aktuell wird hier die auth_user_id des eingeloggten Benutzers
# aus einem JWT Access Token gelesen.
#
# Die technische JWT-Prüfung liegt im shared-Bereich:
# shared/auth/jwt.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from shared.auth.jwt import decode_access_token


# HTTPBearer liest den Authorization-Header aus.
# Erwartetes Format:
# Authorization: Bearer <token>
bearer_scheme = HTTPBearer()


# Ermittelt die Auth-User-ID aus einem gültigen JWT Access Token.
# Bei fehlendem, ungültigem oder abgelaufenem Token wird die Anfrage abgelehnt.
def get_current_auth_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> int:
    token = credentials.credentials

    auth_user_id = decode_access_token(
        token=token,
        secret_key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    if auth_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    return auth_user_id
