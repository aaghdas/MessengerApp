from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


# SQLAlchemy-Modell für die users-Tabelle.
# Diese Klasse beschreibt, wie Benutzer in PostgreSQL gespeichert werden.
#Das ist ein SQLAlchemy-Modell. Es beschreibt die Datenbanktabelle users.

#Das ist ein SQLAlchemy-Modell. Es beschreibt die Datenbanktabelle users.
class User(Base):
    __tablename__ = "users"

    # Primärschlüssel der Tabelle.
    # Jeder Benutzer bekommt eine eindeutige ID.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Eindeutiger Benutzername.
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)

    # Eindeutige E-Mail-Adresse.
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)

    # Gehashter Passwortwert.
    # Das echte Passwort wird nicht gespeichert.
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Gibt an, ob der Benutzer aktiv ist.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Zeitpunkt der Erstellung.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

# SQLAlchemy-Modell für Passwort-Reset-Codes.
# Diese Tabelle speichert temporäre Codes, mit denen ein Benutzer sein Passwort zurücksetzen kann.
#Weil das Backend später prüfen muss, ob der eingegebene Reset-Code wirklich existiert, zum richtigen Benutzer gehört,
# noch gültig ist und noch nicht benutzt wurde.
#Nach erfolgreichem Reset wird der Code als benutzt markiert: is_used = true
# In dieser Entwicklungsveversion wird der Reset-Code über die API-Response zurückgegeben.
# In einer produktiven Version müsste der Code über einen sicheren Kanal zugestellt werden.
class PasswordResetCode(Base):
    __tablename__ = "password_reset_codes"

    # Primärschlüssel der Tabelle.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ID des Benutzers, für den der Reset-Code erstellt wurde.
    user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    # Reset-Code als Text.
    # Der Code wird später geprüft, bevor ein neues Passwort gesetzt wird.
    code: Mapped[str] = mapped_column(String(20), index=True, nullable=False)

    # Gibt an, ob der Code bereits benutzt wurde.
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Ablaufzeitpunkt des Reset-Codes.
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Zeitpunkt der Erstellung.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)