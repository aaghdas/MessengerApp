"""
erstellen wir das Skript, das die Messaging-Tabellen in PostgreSQL anlegt:

conversations
conversation_members
messages"""
# Hilfsskript zum Erstellen der Messaging-Service-Tabellen.
#
# Diese Datei wird manuell ausgeführt, um alle SQLAlchemy-Modelle
# aus models.py als echte Tabellen in PostgreSQL anzulegen.
#
# Für den Messaging Service werden dadurch aktuell die Tabellen
# conversations, conversation_members und messages
# in der Datenbank messenger_messages erstellt.
#
# Später kann dieses einfache Skript durch Alembic-Migrationen ersetzt werden.

import asyncio

from app.database import Base, engine
from app.models import Conversation, ConversationMember, Message


# Erstellt alle Tabellen, die über SQLAlchemy-Modelle definiert wurden.
async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())