from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


# Die Engine enthält die Verbindungskonfiguration zur PostgreSQL-Datenbank.
# Die Datenbankadresse wird aus der .env Datei über settings.DATABASE_URL geladen.
# echo=True zeigt die ausgeführten SQL-Befehle im Terminal an.
engine = create_async_engine(settings.DATABASE_URL, echo=True)


# AsyncSessionLocal ist eine Session-Fabrik.
# Damit werden später einzelne Datenbank-Sessions erzeugt.
AsyncSessionLocal = sessionmaker(
    # Die Session wird mit der oben erstellten Datenbank-Engine verbunden.
    # Dadurch weiß SQLAlchemy, welche PostgreSQL-Datenbank benutzt werden soll.
    bind=engine,

    # Es werden asynchrone Datenbank-Sessions erstellt.
    # Dadurch können Datenbankoperationen später mit await ausgeführt werden.
    class_=AsyncSession,

    # Nach einem commit bleiben die geladenen Objektwerte verfügbar.
    # Das ist praktisch, wenn nach dem Speichern direkt Daten zurückgegeben werden sollen.
    expire_on_commit=False,
)
"""
bind=engine
→ verbindet die Session mit deiner PostgreSQL-Datenbank

class_=AsyncSession
→ benutzt async Sessions für FastAPI

expire_on_commit=False
→ Daten bleiben nach dem Speichern im Python-Objekt lesbar
"""


# Base ist die Basisklasse für alle SQLAlchemy-Modelle.
#Das bedeutet: SQLAlchemy bekommt eine gemeinsame Basis, über die es alle Tabellenmodelle sammelt.
# Jede Tabellenklasse, z. B. Profile oder Contact, erbt später von Base.
Base = declarative_base()


# get_db ist eine FastAPI-Dependency für Datenbankzugriff.
# Für jede Anfrage wird eine Datenbank-Session geöffnet
# und nach der Anfrage automatisch wieder geschlossen.
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session