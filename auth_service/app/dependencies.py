from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.security import decode_access_token

"""
routes.py definiert die Auth-API-Endpunkte.
Token-Prüfung wird über dependencies.py genutzt; JWT- und Passwortlogik liegt in security.py.
routes.py
→ API-Endpunkte definieren
→ Request entgegennehmen
→ Response zurückgeben

dependencies.py
→ eingeloggten Benutzer ermitteln
→ Token prüfen
→ User aus Datenbank laden

security.py
→ Passwort hashen
→ Passwort prüfen
→ JWT erstellen/dekodieren
"""
# HTTPBearer liest den Authorization-Header aus.
# Erwartetes Format:
# Authorization: Bearer <token>
bearer_scheme = HTTPBearer()


# Dependency zum Abrufen des aktuell eingeloggten Benutzers.
# Das JWT wird geprüft, die Benutzer-ID wird gelesen,
# und der passende Benutzer wird aus der Datenbank geladen.
async def get_current_auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials

    user_id = decode_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user