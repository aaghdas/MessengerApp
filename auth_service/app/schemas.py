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