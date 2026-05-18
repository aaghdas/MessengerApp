#routes.py enthält die Funktionen, die auf HTTP-Anfragen wie Login, Register und Current User reagieren.Also enthält alle funktionen, die die API-Anfragen bearbeiten.
#Dies ist ein Objekt der FastAPI-Klasse APIRouter
#APIRouter ermöglicht es, Routen in modularen Einheiten zu organisieren.
#Hier werden später die Endpoints für die Authentifizierung definiert.
#Die Routen werden in der main.py Datei in die FastAPI-Anwendung eingebunden.
#APIRouter wird verwendet, um zusammengehörige API-Endpunkte in einer eigenen Datei zu gruppieren.
# In diesem Fall werden alle Authentifizierungs-Routen wie Registrierung, Login und aktueller Benutzer in routes.py gesammelt.

from fastapi import APIRouter, Depends, HTTPException, status
#from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
#from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

#from app.config import settings
from app.database import get_db
from app.models import PasswordResetCode, User
from app.schemas import (
    TokenResponse, 
    UserLogin, 
    UserRegister,
     UserResponse,
     PasswordResetConfirm,
     PasswordResetRequest,
     PasswordResetRequestResponse
)
from app.security import (
    create_access_token, 
    hash_password, 
    verify_password,
    create_password_reset_code)
# from app.security importdecode_access_token
from app.dependencies import get_current_auth_user
from datetime import datetime, timedelta
from app.models import PasswordResetCode, User



# APIRouter sammelt die Auth-Endpunkte in einer eigenen Router-Gruppe.
# Alle Routen in dieser Datei beginnen mit /auth.
# In der FastAPI-Dokumentation werden sie unter dem Tag "Auth" angezeigt.
router = APIRouter(prefix="/auth", tags=["Auth"])


# HTTPBearer liest den Authorization-Header aus.
# Erwartetes Format:
# Authorization: Bearer <token>
#bearer_scheme = HTTPBearer()    jetzt in dependencies.py


# Registrierung eines neuen Benutzers.
# Erwartet username, email und password im Request Body.
# Gibt die gespeicherten Benutzerdaten ohne Passwort zurück.
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    # Prüfung, ob der Benutzername bereits existiert.
    existing_username_result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    existing_username = existing_username_result.scalar_one_or_none()

    # Bei bereits vorhandenem Benutzernamen wird die Registrierung abgebrochen.
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already registered.",
        )

    # Prüfung, ob die E-Mail-Adresse bereits existiert.
    existing_email_result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_email = existing_email_result.scalar_one_or_none()

    # Bei bereits vorhandener E-Mail-Adresse wird die Registrierung abgebrochen.
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    # Neues User-Objekt wird erstellt.
    # Das Klartext-Passwort wird nicht gespeichert.
    # Stattdessen wird nur der Passwort-Hash gespeichert.
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    # Neuer Benutzer wird zur aktuellen Datenbank-Session hinzugefügt.
    db.add(new_user)

    # Änderungen werden dauerhaft in PostgreSQL gespeichert.
    await db.commit()

    # Das Python-Objekt wird mit den Daten aus der Datenbank aktualisiert.
    # Dadurch sind z. B. id und created_at verfügbar.
    await db.refresh(new_user)

    return new_user


# Login eines bestehenden Benutzers.
# Erwartet email und password im Request Body.
# Gibt bei Erfolg ein JWT Access Token zurück.
@router.post("/login", response_model=TokenResponse)
async def login_user(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    # Benutzer wird anhand der E-Mail-Adresse gesucht.
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()

    # Login wird abgelehnt, wenn kein Benutzer gefunden wurde
    # oder wenn das Passwort nicht zum gespeicherten Hash passt.
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    # JWT Access Token wird erstellt.
    # sub enthält die Benutzer-ID als eindeutige Token-Identität.
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
        }
    )

    return TokenResponse(access_token=access_token)

"""
# Gibt den aktuell eingeloggten Benutzer zurück.
# Dafür muss ein gültiges Bearer Token im Authorization-Header gesendet werden.

@router.get("/current-user", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    # Token wird aus dem Authorization-Header gelesen.
    token = credentials.credentials

    try:
        # JWT wird geprüft und dekodiert.
        # Dabei werden Secret Key und Algorithmus aus der .env-Konfiguration verwendet.
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        # sub enthält die Benutzer-ID, die beim Login in das Token geschrieben wurde.
        user_id = payload.get("sub")

        # Ein Token ohne Benutzer-ID ist ungültig.
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
            )

    # JWTError wird ausgelöst, wenn das Token ungültig, manipuliert oder abgelaufen ist.
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    # Benutzer wird anhand der ID aus dem Token in der Datenbank gesucht.
    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()

    # Falls kein Benutzer zur Token-ID existiert, wird 404 zurückgegeben.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user
"""
#@router.get("/current-user", response_model=UserResponse) async def get_current_user(...) geändert.
#Vorher war in routes.py alles direkt drin.Das heißt, routes.py musste selbst wissen, wie ein JWT geprüft wird.
#in neue funktion wurde diese Arbeit nach security.py verschoben->in security.py:  decode_access_token(token)
#Darum soll get_current_user() nicht mehr selbst jwt.decode(...) machen, sondern nur noch sagen: user_id = decode_access_token(token)
"""
Vorher routes.py macht zu viel: Route + Token prüfen + Token dekodieren + User suchen
Nachher Aufgaben sind sauber getrennt:
security.py → Token erstellen und prüfen
routes.py → API-Anfragen bearbeiten und User aus DB holen
"""

"""
# Gibt den aktuell eingeloggten Benutzer zurück.
# Dafür muss ein gültiges Bearer Token im Authorization-Header gesendet werden.
@router.get("/current-user", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    # Token wird aus dem Authorization-Header gelesen.
    token = credentials.credentials

    # Token wird geprüft und die Benutzer-ID wird aus dem Token gelesen.
    user_id = decode_access_token(token)

    # Wenn keine Benutzer-ID gelesen werden kann, ist das Token ungültig.
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
        )

    # Benutzer wird anhand der ID aus dem Token in der Datenbank gesucht.
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    # Falls kein Benutzer zur Token-ID existiert, wird 404 zurückgegeben.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user
"""


"""
Vorher war /auth/current-user verantwortlich für:
Token lesen
Token prüfen
User-ID lesen
User aus Datenbank holen
User zurückgeben

Jetzt ist die Route nur noch verantwortlich für: aktuellen User zurückgeben

Die Auth-Logik ist zentral in: dependencies.py
"""
# Gibt den aktuell eingeloggten Benutzer zurück.
# Die Token-Prüfung und das Laden des Benutzers werden über get_current_auth_user ausgeführt.
@router.get("/current-user", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(get_current_auth_user),
):
    return current_user


# Erstellt einen Passwort-Reset-Code für einen bestehenden Benutzer.
# In dieser Entwicklungs-/Abgabeversion wird der Code direkt in der API-Response zurückgegeben.
@router.post(
    "/password-reset/request",
    response_model=PasswordResetRequestResponse,
)
async def request_password_reset(
    reset_data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.email == reset_data.email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    reset_code = create_password_reset_code()
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    password_reset_code = PasswordResetCode(
        user_id=user.id,
        code=reset_code,
        expires_at=expires_at,
    )

    db.add(password_reset_code)
    await db.commit()

    return PasswordResetRequestResponse(
        message="Password reset code created.",
        reset_code=reset_code,
    )


# Bestätigt einen Passwort-Reset mit E-Mail, Reset-Code und neuem Passwort.
# Der Code muss gültig, nicht abgelaufen und noch nicht benutzt sein.
@router.post("/password-reset/confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db),
):
    user_result = await db.execute(
        select(User).where(User.email == reset_data.email)
    )
    user = user_result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    code_result = await db.execute(
        select(PasswordResetCode).where(
            PasswordResetCode.user_id == user.id,
            PasswordResetCode.code == reset_data.reset_code,
            PasswordResetCode.is_used == False,
        )
    )
    password_reset_code = code_result.scalar_one_or_none()

    if not password_reset_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset code.",
        )

    if password_reset_code.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset code has expired.",
        )

    user.hashed_password = hash_password(reset_data.new_password)
    password_reset_code.is_used = True

    await db.commit()

    return {
        "message": "Password has been reset successfully."
    }