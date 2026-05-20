# Hilfsskript zum Erstellen der User-Service-Tabellen.
#
# Diese Datei wird manuell ausgeführt, um alle SQLAlchemy-Modelle
# aus models.py als echte Tabellen in PostgreSQL anzulegen.
#
# Für den User Service werden dadurch aktuell die Tabellen
# profiles und contacts in der Datenbank messenger_user erstellt.
#
# Später kann dieses einfache Skript durch Alembic-Migrationen ersetzt werden.

import asyncio

from app.database import Base, engine
from app.models import Contact, Profile


# Erstellt alle Tabellen, die über SQLAlchemy-Modelle definiert wurden.
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())

"""create_tables.py ist ein Hilfsskript, um die Tabellen für den User Service in PostgreSQL zu erstellen.
test in terminal:
cd ~/messenger-app/user_service # wechsle in das Verzeichnis des User Service
source venv/bin/activate # aktiviere die virtuelle Umgebung
python -m app.create_tables # führt das Skript aus und erstellt die Tabellen in der Datenbank messenger_user
psql -h localhost -U postgres -d messenger_user   # verbindet sich mit der Datenbank messenger_user über die psql-Konsole
password: messenger_dev_123
\dt  # zeigt die Tabellen in der Datenbank messenger_user
\d profiles  # zeigt die Spalten der Tabelle profiles
\d contacts
\q  # verlässt die psql-Konsole

\dt
            List of tables
 Schema |   Name   | Type  |  Owner   
--------+----------+-------+----------
 public | contacts | table | postgres
 public | profiles | table | postgres
(2 rows)

 \d profiles
                                         Table "public.profiles"
    Column    |            Type             | Collation | Nullable |               Default                
--------------+-----------------------------+-----------+----------+--------------------------------------
 id           | integer                     |           | not null | nextval('profiles_id_seq'::regclass)
 auth_user_id | integer                     |           | not null | 
 display_name | character varying(100)      |           | not null | 
 bio          | character varying(255)      |           |          | 
 avatar_url   | character varying(500)      |           |          | 
 created_at   | timestamp without time zone |           | not null | 
Indexes:
    "profiles_pkey" PRIMARY KEY, btree (id)
    "ix_profiles_auth_user_id" UNIQUE, btree (auth_user_id)
    "ix_profiles_id" btree (id)
"""
