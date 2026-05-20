#Diese Datei wird verwendet, um die Datenbanktabellen zu erstellen, die von den SQLAlchemy-Modellen beschrieben werden.

import asyncio
from app.database import Base, engine
from app.models import User,PasswordResetCode


# Erstellt alle Tabellen, die von SQLAlchemy-Modellen(models.py) beschrieben werden.
# Aktuell wird dadurch die users-Tabelle erstellt.
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

#Führe den folgenden Code nur aus, wenn diese Datei direkt gestartet wird.
#Also bei: python -m app.create_tables. Aber nicht, wenn die Datei nur importiert wird.
if __name__ == "__main__":
    asyncio.run(create_tables())


"""Diese Datei wird verwendet, um die Datenbanktabellen zu erstellen, die von den SQLAlchemy-Modellen beschrieben werden.
models.py beschreibt die Tabelle
create_tables.py liest diese Beschreibung
SQLAlchemy erzeugt daraus CREATE TABLE SQL
PostgreSQL erstellt die echte Tabelle in der Datenbank, wenn diese Datei ausgeführt wird."""


"""
async def create_tables(): => Erstelle eine asynchrone Funktion namens create_tables.
Diese Funktion ist asynchron. Das heißt: Die Funktion kann mit Operationen arbeiten, die Zeit brauchen, zum Beispiel:

Datenbankverbindung öffnen
SQL-Befehle ausführen
auf PostgreSQL warten

Weil Datenbankverbindung mit AsyncSession und create_async_engine arbeitet, schreiben wir hier auch async.

async with engine.begin() as connection: => with bedeutet allgemein:

Öffne eine Ressource sauber und schließe sie danach automatisch wieder.
async with ist die asynchrone Version davon, weil die Datenbankverbindung async ist.

Öffne die Datenbankverbindung.
Benutze sie.
Schließe sie danach automatisch.
 
engine kommt aus deiner Datei database.py.
engine = Verbindungsmotor zur Datenbank


engine.begin() öffnet eine Datenbankverbindung und startet eine Transaktion.

async with engine.begin() as connection: as connection bedeutet:

Speichere die geöffnete Datenbankverbindung in der Variable connection.

Danach können wir diese Verbindung benutzen:

connection.run_sync(...)

Also connection = aktive Verbindung zu PostgreSQL

await
await connection.run_sync(...)

await bedeutet: Warte, bis diese asynchrone Operation fertig ist.

Da Datenbankarbeit nicht sofort passiert, sondern PostgreSQL antworten muss, wartet Python hier korrekt auf das Ergebnis.

Ohne await würde die Operation nicht richtig ausgeführt werden.

connection.run_sync(...)
connection.run_sync(Base.metadata.create_all)

Datenbankverbindung ist async. Aber Base.metadata.create_all ist eine normale synchrone SQLAlchemy-Funktion.

run_sync bedeutet:Führe diese synchrone SQLAlchemy-Funktion innerhalb der async Verbindung aus.

Also run_sync ist hier eine Brücke: async Datenbankverbindung + synchrone create_all Funktion

Base
Base.metadata.create_all => Base kommt aus database.py:

Base = declarative_base()

Alle Models erben von Base, zum Beispiel:

class User(Base):
    __tablename__ = "users"

Dadurch kennt Base alle Tabellenmodelle. Base sammelt alle SQLAlchemy-Modelle.

metadata
Base.metadata
metadata ist die Sammlung aller Tabelleninformationen.

Darin steht zum Beispiel:
Tabelle: users
Spalten: id, username, email, hashed_password

Also: metadata = Bauplan aller Tabellen
13. create_all
Base.metadata.create_all

create_all bedeutet: Erstelle alle Tabellen aus dem Bauplan, falls sie noch nicht existieren.

Beispiel:

Wenn in models.py steht:

class Message(Base):
    __tablename__ = "messages"

dann kann create_all daraus in PostgreSQL machen:

CREATE TABLE messages (...)

Wichtig:

create_all erstellt fehlende Tabellen.
Es löscht keine Tabellen.
Es ändert keine Tabellen, wenn sich die Models ändern.

Erstelle eine asynchrone Funktion namens create_tables.

async with engine.begin() as connection:

Öffne eine Datenbankverbindung und starte eine Transaktion. speichere die Verbindung in der Variable connection.

await connection.run_sync(Base.metadata.create_all) Führe die synchrone Funktion create_all innerhalb der async Verbindung aus
und warte auf das Ergebnis. Warte darauf, dass SQLAlchemy alle Tabellen aus den Models in PostgreSQL erstellt.

"""