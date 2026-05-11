from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# SQLAlchemy-Modell für die users-Tabelle.
# Diese Klasse beschreibt, wie Benutzer in PostgreSQL gespeichert werden.
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