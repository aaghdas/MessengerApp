from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

#Diese klasse erstellt die Pydantic-Schemas für den Auth Service.
#Schemas beschreiben, welche Daten eine API erwartet und welche Daten sie zurückgibt.
# Schema für die Registrierung.Diese Daten werden vom Client beim Registrieren gesendet.
class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


# Schema für den Login.
# Diese Daten werden vom Client beim Einloggen gesendet.
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema für Benutzerdaten in API-Antworten.
# Das Passwort oder hashed_password wird absichtlich nicht zurückgegeben.
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# Schema für die Token-Antwort nach erfolgreichem Login.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Schema zum Anfordern eines Passwort-Reset-Codes.
# Der Benutzer gibt seine E-Mail-Adresse an.
#Die E-Mail-Adresse wird verwendet, um den passenden Benutzer zu finden.
# In dieser Entwicklungs-/Abgabeversion wird der Reset-Code nicht per E-Mail verschickt,
# sondern direkt in der API-Response zurückgegeben.
# In einer späteren Version kann der Code über einen sicheren Kanal zugestellt werden, z.B. per Email.
class PasswordResetRequest(BaseModel):
    email: EmailStr


# Schema für die Antwort nach dem Erstellen eines Reset-Codes.
# Der Reset-Code wird aktuell für Testzwecke direkt zurückgegeben.
# Später sollte der Code nicht mehr in der Response stehen,
# sondern über einen sicheren Zustellweg gesendet werden.
class PasswordResetRequestResponse(BaseModel):
    message: str
    reset_code: str


# Schema zum Bestätigen eines Passwort-Resets.
# Der Benutzer sendet E-Mail, Reset-Code und neues Passwort.
class PasswordResetConfirm(BaseModel):
    email: EmailStr
    reset_code: str = Field(min_length=4, max_length=20)
    new_password: str = Field(min_length=8, max_length=128)