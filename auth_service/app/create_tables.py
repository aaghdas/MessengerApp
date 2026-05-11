import asyncio

from app.database import Base, engine
from app.models import User


# Erstellt alle Tabellen, die von SQLAlchemy-Modellen(models.py) beschrieben werden.
# Aktuell wird dadurch die users-Tabelle erstellt.
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())


"""Diese Datei wird verwendet, um die Datenbanktabellen zu erstellen, die von den SQLAlchemy-Modellen beschrieben werden.
models.py beschreibt die Tabelle
create_tables.py liest diese Beschreibung
SQLAlchemy erzeugt daraus CREATE TABLE SQL
PostgreSQL erstellt die echte Tabelle in der Datenbank, wenn diese Datei ausgeführt wird."""