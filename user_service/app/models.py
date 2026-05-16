from datetime import datetime

from sqlalchemy import DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# SQLAlchemy-Modell für die profiles-Tabelle.
# Diese Tabelle speichert öffentliche Profilinformationen eines Benutzers.
class Profile(Base):
    __tablename__ = "profiles"

    # Primärschlüssel der Tabelle.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ID des Benutzers aus dem Auth Service.
    # Es wird bewusst keine direkte Foreign-Key-Beziehung zur Auth-Datenbank erstellt,
    # weil jeder Microservice seine eigene Datenbank besitzt.
    auth_user_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        index=True,
        nullable=False,
    )

    # Anzeigename des Benutzers.
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Optionaler kurzer Profiltext.
    bio: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Optionaler Avatar-Link.
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Zeitpunkt der Profilerstellung.
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


# SQLAlchemy-Modell für die contacts-Tabelle.
# Diese Tabelle speichert Kontaktbeziehungen zwischen Benutzern.
class Contact(Base):
    __tablename__ = "contacts"

    # Kombination aus owner_user_id und contact_user_id muss eindeutig sein.
    # Dadurch kann derselbe Kontakt nicht doppelt gespeichert werden.
    __table_args__ = (
        UniqueConstraint(
            "owner_user_id",
            "contact_user_id",
            name="unique_contact_pair",
        ),
    )

    # Primärschlüssel der Tabelle.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ID des Benutzers, dem die Kontaktliste gehört.
    owner_user_id: Mapped[int] = mapped_column(
        Integer,
        index=True,
        nullable=False,
    )

    # ID des Benutzers, der als Kontakt gespeichert wird.
    contact_user_id: Mapped[int] = mapped_column(
        Integer,
        index=True,
        nullable=False,
    )

    # Zeitpunkt der Erstellung des Kontakts.
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

"""models.py bedeutet Datenbank-Modelle, d.h.Python-Beschreibung der Datenbanktabellen.
Ein Model beschreibt in Python, wie eine Tabelle in PostgreSQL aussehen soll.

Zum Beispiel:
class Profile(Base):
    __tablename__ = "profiles"
bedeutet: Erstelle/beschreibe eine Tabelle namens profiles.
Und display_name: Mapped[str] = mapped_column(String(100), nullable=False)
bedeutet: Die Tabelle profiles hat eine Spalte display_name.
Sie ist Text, maximal 100 Zeichen, und darf nicht leer sein.
In deinem User Service user_service/app/models.py beschreibt diese Tabellen:
profiles
contacts
Profile  → Profilinformationen eines Benutzers
Contact  → Kontaktbeziehungen zwischen Benutzern
Warum brauchen wir Models?
Damit SQLAlchemy weiß:
Welche Tabellen gibt es?
Welche Spalten gibt es?
Welche Datentypen haben die Spalten?
Welche Werte müssen eindeutig sein?
"""