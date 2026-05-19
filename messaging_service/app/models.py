"""
Datenbankmodelle für den Messaging Service:

conversations
conversation_members
messages"""
# SQLAlchemy-Modelle für den Messaging Service.
#
# Diese Datei beschreibt die Datenbanktabellen für Chats und Nachrichten.
# Der Messaging Service speichert Conversations, Mitglieder einer Conversation
# und einzelne Nachrichten in der Datenbank messenger_messages.

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# Tabelle für einzelne Chats/Conversations.
# Eine Conversation kann später ein 1-zu-1-Chat oder ein Gruppenchat sein.
class Conversation(Base):
    __tablename__ = "conversations"

    # Primärschlüssel der Conversation.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Optionaler Name der Conversation.
    # Bei 1-zu-1-Chats kann dieser Wert leer sein.
    title: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # ID des Benutzers, der die Conversation erstellt hat.
    created_by_user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    # Zeitpunkt der Erstellung.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


# Tabelle für Mitglieder einer Conversation.
# Hier wird gespeichert, welche Benutzer zu welchem Chat gehören.
class ConversationMember(Base):
    __tablename__ = "conversation_members"

    # Ein Benutzer darf pro Conversation nur einmal Mitglied sein.
    __table_args__ = (
        UniqueConstraint(
            "conversation_id",
            "user_id",
            name="unique_conversation_member",
        ),
    )

    # Primärschlüssel des Mitglied-Datensatzes.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ID der Conversation.
    conversation_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    # Auth-User-ID des Mitglieds.
    user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    # Zeitpunkt, wann der Benutzer zur Conversation hinzugefügt wurde.
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


# Tabelle für einzelne Nachrichten.
# Jede Nachricht gehört zu einer Conversation und hat einen Sender.
class Message(Base):
    __tablename__ = "messages"

    # Primärschlüssel der Nachricht.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ID der Conversation, zu der diese Nachricht gehört.
    conversation_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    # Auth-User-ID des Senders.
    sender_user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    # Textinhalt der Nachricht.
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Zeitpunkt, zu dem die Nachricht erstellt wurde.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)