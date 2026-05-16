# Pydantic-Schemas für den User Service.
# Diese Klassen definieren die Datenstruktur für API-Requests und API-Responses.
# Sie legen fest, welche Felder vom Client gesendet werden dürfen,
# welche Felder optional sind und welche Datentypen erwartet werden.
# Die Schemas werden von FastAPI automatisch zur Validierung genutzt.
# Ungültige Daten, z. B. zu kurze Namen oder falsche Datentypen,
# werden dadurch direkt mit einer passenden Fehlermeldung abgelehnt.
# Außerdem wird über Response-Schemas kontrolliert,
# welche Daten an den Client zurückgegeben werden.
# Dadurch bleiben interne Datenbankdetails vom API-Output getrennt.
from datetime import datetime
from pydantic import BaseModel, Field


# Schema zum Erstellen eines Profils.
# Diese Daten werden vom Client an den User Service gesendet.
class ProfileCreate(BaseModel):
    auth_user_id: int
    display_name: str = Field(min_length=2, max_length=100)
    bio: str | None = Field(default=None, max_length=255)
    avatar_url: str | None = Field(default=None, max_length=500)


# Schema zum Aktualisieren eines Profils.
# Alle Felder sind optional, damit einzelne Profilwerte geändert werden können.
class ProfileUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=2, max_length=100)
    bio: str | None = Field(default=None, max_length=255)
    avatar_url: str | None = Field(default=None, max_length=500)


# Schema für Profilantworten.
# Dieses Schema wird verwendet, wenn ein Profil an den Client zurückgegeben wird.
class ProfileResponse(BaseModel):
    id: int
    auth_user_id: int
    display_name: str
    bio: str | None
    avatar_url: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# Schema zum Erstellen eines Kontakts.
# owner_user_id ist der Benutzer, dem die Kontaktliste gehört.
# contact_user_id ist der Benutzer, der als Kontakt gespeichert wird.
class ContactCreate(BaseModel):
    owner_user_id: int
    contact_user_id: int


# Schema für Kontaktantworten.
# Dieses Schema wird verwendet, wenn ein Kontakt an den Client zurückgegeben wird.
class ContactResponse(BaseModel):
    id: int
    owner_user_id: int
    contact_user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }