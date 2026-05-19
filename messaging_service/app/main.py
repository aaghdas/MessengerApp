# Haupteinstiegspunkt für den Messaging Service.
#
# Diese Datei erstellt die FastAPI-Anwendung, bindet CORS ein,
# registriert REST-Routen und enthält den WebSocket-Endpunkt
# für Echtzeitnachrichten.
#
# REST-Routen liegen in routes.py.
# WebSocket-Verbindungsverwaltung liegt in websocket.py.
# Datenbankverbindung liegt in database.py.

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import ConversationMember, Message
from app.routes import router as messaging_router
from app.websocket import manager
from shared.auth.jwt import decode_access_token
from app.config import settings


# FastAPI-Anwendung für den Messaging Service.
app = FastAPI(title="Messaging Service")


# CORS-Konfiguration für lokale Entwicklung.
# Dadurch darf das React-Frontend später Anfragen an diesen Service senden.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# REST-Router wird eingebunden.
# Dadurch werden Endpunkte wie /conversations und /messages verfügbar.
app.include_router(messaging_router)


# Einfacher Health-Check-Endpunkt.
# Damit kann geprüft werden, ob der Messaging Service läuft.
@app.get("/")
def root():
    return {
        "service": "messaging_service",
        "status": "running"
    }


# WebSocket-Endpunkt für Echtzeitnachrichten in einer Conversation.
#
# Der Token wird als Query-Parameter übergeben:
# ws://127.0.0.1:8003/ws/conversations/1?token=<JWT_TOKEN>
#
# Ablauf:
# 1. Token wird geprüft.
# 2. User-ID wird aus dem Token gelesen.
# 3. Es wird geprüft, ob der User Mitglied der Conversation ist.
# 4. WebSocket-Verbindung wird akzeptiert.
# 5. Eingehende Nachrichten werden gespeichert und an verbundene Clients gesendet.
@app.websocket("/ws/conversations/{conversation_id}")
async def websocket_conversation(
    websocket: WebSocket,
    conversation_id: int,
    token: str,
):
    auth_user_id = decode_access_token(
        token=token,
        secret_key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    if auth_user_id is None:
        await websocket.close(code=1008)
        return

    async with AsyncSessionLocal() as db:
        member_result = await db.execute(
            select(ConversationMember).where(
                ConversationMember.conversation_id == conversation_id,
                ConversationMember.user_id == auth_user_id,
            )
        )
        member = member_result.scalar_one_or_none()

        if not member:
            await websocket.close(code=1008)
            return

        await manager.connect(conversation_id, websocket)

        try:
            while True:
                data = await websocket.receive_json()
                content = data.get("content")

                if not content:
                    continue

                new_message = Message(
                    conversation_id=conversation_id,
                    sender_user_id=auth_user_id,
                    content=content,
                )

                db.add(new_message)
                await db.commit()
                await db.refresh(new_message)

                await manager.broadcast(
                    conversation_id,
                    {
                        "id": new_message.id,
                        "conversation_id": new_message.conversation_id,
                        "sender_user_id": new_message.sender_user_id,
                        "content": new_message.content,
                        "created_at": new_message.created_at.isoformat(),
                    },
                )

        except WebSocketDisconnect:
            manager.disconnect(conversation_id, websocket)