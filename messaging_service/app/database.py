# Datenbankverbindung für den Messaging Service.
#
# Diese Datei erstellt die Verbindung zur PostgreSQL-Datenbank
# messenger_messages und stellt eine wiederverwendbare Datenbank-Session
# für API-Routen und WebSocket-Logik bereit.

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


# Die Engine enthält die Verbindungskonfiguration zur PostgreSQL-Datenbank.
# Die Datenbankadresse wird aus messaging_service/.env geladen.
# echo=True zeigt SQL-Befehle im Terminal an und ist für Entwicklung hilfreich.
engine = create_async_engine(settings.DATABASE_URL, echo=True)


# AsyncSessionLocal ist eine Session-Fabrik.
# Damit werden später einzelne asynchrone Datenbank-Sessions erzeugt.
AsyncSessionLocal = sessionmaker(
    # Die Session wird mit der oben erstellten Datenbank-Engine verbunden.
    bind=engine,

    # Es werden asynchrone Datenbank-Sessions erstellt.
    class_=AsyncSession,

    # Nach einem commit bleiben Objektwerte verfügbar.
    expire_on_commit=False,
)


# Base ist die Basisklasse für alle SQLAlchemy-Modelle.
# Conversation, ConversationMember und Message erben später von Base.
Base = declarative_base()


# FastAPI-Dependency für Datenbankzugriff.
# Für jede Anfrage wird eine Session geöffnet und danach automatisch geschlossen.
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session