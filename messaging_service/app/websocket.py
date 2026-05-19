# WebSocket-Logik für den Messaging Service.
#WebSocket ermöglicht Echtzeit-Kommunikation.
# Im Gegensatz zu normalen HTTP-Requests bleibt die Verbindung offen, sodass neue Nachrichten sofort an verbundene Clients gesendet werden können.
#
# Diese Datei enthält einen einfachen Connection Manager für Echtzeitkommunikation.
# Clients verbinden sich später mit einer Conversation und können Nachrichten
# in Echtzeit senden und empfangen.
#
# Die Speicherung der Nachrichten in PostgreSQL wird später über die WebSocket-Route
# mit der Message-Tabelle verbunden.

from fastapi import WebSocket


# Verwaltet aktive WebSocket-Verbindungen pro Conversation.
class ConnectionManager:
    def __init__(self):
        # Dictionary:
        # conversation_id -> Liste aktiver WebSocket-Verbindungen
        #Dieses ConnectionManager-Objekt bekommt eine eigene Variable active_connections.
        #Darin werden alle aktiven WebSocket-Verbindungen gespeichert.
        self.active_connections: dict[int, list[WebSocket]] = {}

    # Neue WebSocket-Verbindung akzeptieren und speichern.
    async def connect(self, conversation_id: int, websocket: WebSocket):
        await websocket.accept()

        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = []

        self.active_connections[conversation_id].append(websocket)

    # WebSocket-Verbindung aus der aktiven Liste entfernen.
    def disconnect(self, conversation_id: int, websocket: WebSocket):
        if conversation_id in self.active_connections:
            self.active_connections[conversation_id].remove(websocket)

            if not self.active_connections[conversation_id]:
                del self.active_connections[conversation_id]

    # Nachricht an alle verbundenen Clients einer Conversation senden.
    async def broadcast(self, conversation_id: int, message: dict):
        if conversation_id not in self.active_connections:
            return

        for connection in self.active_connections[conversation_id]:
            await connection.send_json(message)


# Globale Connection-Manager-Instanz.
# Diese wird später in main.py oder routes.py für WebSocket-Endpunkte verwendet.
manager = ConnectionManager()

"""
WebSocket ist eine Verbindung zwischen Client und Server, die offen bleibt.
Bei normalem HTTP passiert das:Client fragt → Server antwortet → Verbindung endet
Beispiel: GET /messages
Der Client muss immer wieder neu fragen, ob neue Nachrichten da sind.
Bei WebSocket passiert das:
Client verbindet sich → Verbindung bleibt offen → beide Seiten können jederzeit senden
Das ist wichtig für Messenger-Apps.
Beispiel Messenger
1. Ohne WebSocket:
User A sendet Nachricht
User B sieht sie erst, wenn er aktualisiert oder erneut lädt
2.Mit WebSocket:
User A sendet Nachricht
Server schickt sie sofort live an User B
User B sieht die Nachricht direkt
"""