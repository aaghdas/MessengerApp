# Pydantic-Schemas für den Messaging Service.
#
# Diese Datei definiert die Datenstruktur für API-Requests und API-Responses.
# Sie legt fest, welche Daten beim Erstellen von Conversations und Messages
# gesendet werden dürfen und welche Daten die API zurückgibt.

from datetime import datetime

from pydantic import BaseModel, Field


# Schema zum Erstellen einer Conversation.
# member_user_ids enthält die Benutzer, die zusätzlich zum eingeloggten User
# in die Conversation aufgenommen werden sollen.
class ConversationCreate(BaseModel):
    title: str | None = Field(default=None, max_length=100)
    member_user_ids: list[int] = Field(min_length=1)


# Schema für Conversation-Antworten.
class ConversationResponse(BaseModel):
    id: int
    title: str | None
    created_by_user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# Schema für Mitglieder einer Conversation.
class ConversationMemberResponse(BaseModel):
    id: int
    conversation_id: int
    user_id: int
    joined_at: datetime

    model_config = {
        "from_attributes": True
    }


# Schema zum Erstellen einer Nachricht.
# sender_user_id wird nicht vom Client gesendet,
# sondern aus dem JWT Access Token gelesen.
class MessageCreate(BaseModel):
    conversation_id: int
    content: str = Field(min_length=1, max_length=5000)


# Schema für Message-Antworten.
class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_user_id: int
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }