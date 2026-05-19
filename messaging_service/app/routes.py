"""
REST-Endpunkte erstellen für:

POST /conversations
GET  /conversations
POST /messages
GET  /conversations/{conversation_id}/messages
"""
# API-Routen für den Messaging Service.
#
# Diese Datei definiert REST-Endpunkte für Conversations und Messages.
# Eingehende API-Anfragen werden verarbeitet, Daten werden über SQLAlchemy
# aus der PostgreSQL-Datenbank gelesen oder gespeichert und passende
# API-Antworten zurückgegeben.
#
# Die eingeloggte User-ID wird aus dem JWT Access Token gelesen.
# sender_user_id und created_by_user_id werden nicht vom Client übernommen.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_auth_user_id
from app.models import Conversation, ConversationMember, Message
from app.schemas import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)


# Router für alle Messaging-Service-Endpunkte.
router = APIRouter(tags=["Messaging Service"])


# Erstellt eine neue Conversation.
# Der eingeloggte Benutzer wird automatisch als Ersteller und Mitglied gespeichert.
@router.post(
    "/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_conversation(
    conversation_data: ConversationCreate,
    auth_user_id: int = Depends(get_current_auth_user_id),
    db: AsyncSession = Depends(get_db),
):
    new_conversation = Conversation(
        title=conversation_data.title,
        created_by_user_id=auth_user_id,
    )

    db.add(new_conversation)
    await db.commit()
    await db.refresh(new_conversation)

    # Ersteller automatisch als Mitglied hinzufügen.
    creator_member = ConversationMember(
        conversation_id=new_conversation.id,
        user_id=auth_user_id,
    )
    db.add(creator_member)

    # Weitere Mitglieder hinzufügen.
    for member_user_id in conversation_data.member_user_ids:
        if member_user_id != auth_user_id:
            member = ConversationMember(
                conversation_id=new_conversation.id,
                user_id=member_user_id,
            )
            db.add(member)

    await db.commit()

    return new_conversation


# Gibt alle Conversations zurück, in denen der eingeloggte Benutzer Mitglied ist.
@router.get("/conversations", response_model=list[ConversationResponse])
async def get_my_conversations(
    auth_user_id: int = Depends(get_current_auth_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Conversation)
        .join(
            ConversationMember,
            Conversation.id == ConversationMember.conversation_id,
        )
        .where(ConversationMember.user_id == auth_user_id)
    )

    conversations = result.scalars().all()

    return conversations


# Erstellt eine neue Nachricht in einer Conversation.
# Der Sender wird aus dem JWT gelesen.
@router.post(
    "/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_message(
    message_data: MessageCreate,
    auth_user_id: int = Depends(get_current_auth_user_id),
    db: AsyncSession = Depends(get_db),
):
    # Prüfen, ob der eingeloggte Benutzer Mitglied der Conversation ist.
    member_result = await db.execute(
        select(ConversationMember).where(
            ConversationMember.conversation_id == message_data.conversation_id,
            ConversationMember.user_id == auth_user_id,
        )
    )
    member = member_result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this conversation.",
        )

    new_message = Message(
        conversation_id=message_data.conversation_id,
        sender_user_id=auth_user_id,
        content=message_data.content,
    )

    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)

    return new_message


# Gibt alle Nachrichten einer Conversation zurück.
# Nur Mitglieder der Conversation dürfen die Nachrichten lesen.
@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
async def get_conversation_messages(
    conversation_id: int,
    auth_user_id: int = Depends(get_current_auth_user_id),
    db: AsyncSession = Depends(get_db),
):
    # Prüfen, ob der eingeloggte Benutzer Mitglied der Conversation ist.
    member_result = await db.execute(
        select(ConversationMember).where(
            ConversationMember.conversation_id == conversation_id,
            ConversationMember.user_id == auth_user_id,
        )
    )
    member = member_result.scalar_one_or_none()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this conversation.",
        )

    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = result.scalars().all()

    return messages