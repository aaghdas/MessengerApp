from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


# Async SQLAlchemy Engine für die Verbindung zur PostgreSQL-Datenbank.
# Die Verbindungsadresse wird aus der .env Datei über settings.DATABASE_URL geladen.
engine = create_async_engine(settings.DATABASE_URL, echo=True)


# SessionLocal erzeugt Datenbank-Sessions.
# Jede Anfrage bekommt später eine eigene Session.
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