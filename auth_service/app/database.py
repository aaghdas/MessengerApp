from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


# Async SQLAlchemy Engine für die Verbindung zur PostgreSQL-Datenbank.
# Die Verbindungsadresse wird aus der .env Datei über settings.DATABASE_URL geladen.
engine = create_async_engine(settings.DATABASE_URL, echo=True)


# AsyncSessionLocal ist eine Session-Fabrik.SessionLocal erzeugt Datenbank-Sessions.
# Damit werden später einzelne Datenbank-Sessions erzeugt.Jede Anfrage bekommt später eine eigene Session.
#   expire_on_commit=False bedeutet, dass die Daten nach einem Commit nicht automatisch ungültig werden.

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Base ist die Basisklasse für alle SQLAlchemy-Modelle.
# Tabellenmodelle wie User erben später von Base.
Base = declarative_base()


# Dependency für FastAPI-Routen.
# Damit kann in Endpoints eine Datenbank-Session verwendet werden.
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session