# Messenger App Progress Documentation

## Überblick

Diese Dokumentation beschreibt den aktuellen Entwicklungsstand der Messenger-App.  
Die Anwendung wird als Microservices-Projekt entwickelt. Das bedeutet, dass verschiedene Aufgaben der App auf mehrere getrennte Services verteilt werden. Jeder Service besitzt eine klare Verantwortung und arbeitet mit seiner eigenen Datenbank.

Aktuell wurden der Auth Service und der User Service aufgebaut. Zusätzlich wurde eine gemeinsame `shared`-Struktur vorbereitet, damit wiederverwendbare Logik, insbesondere JWT-Prüfung, nicht mehrfach in jedem Service geschrieben werden muss.

## Ziel des Projekts

Ziel des Projekts ist der Aufbau einer sicheren, modularen und erweiterbaren Messenger-App. Benutzer sollen sich registrieren, einloggen, Profile verwalten, Kontakte hinzufügen und später in Echtzeit Nachrichten austauschen können.

Das Backend bildet dabei die Grundlage für:
- Benutzerregistrierung und Login
- sichere Passwortspeicherung durch Hashing
- JWT-basierte Authentifizierung
- Benutzerprofile
- Kontaktverwaltung
- spätere Chat- und Messaging-Funktionen
- spätere WebSocket-Kommunikation
- spätere Verbindung mit einem React Frontend

## Aktueller Stand

✅ Auth Service fertig  
✅ User Service fertig  
🟡 Messaging Service offen  
🔴 Frontend offen

- Einrichtung der Projektstruktur
- Einrichtung von WSL, VS Code, Python, Node.js und PostgreSQL
- Erstellung mehrerer PostgreSQL-Datenbanken
- Aufbau des Auth Service
- Aufbau des User Service
- Einführung gemeinsamer JWT-Prüfung im `shared`-Ordner
- manuelle API-Tests über FastAPI Swagger UI
- Git/GitHub-Versionierung

Der Messaging Service, das React Frontend, WebSocket-Kommunikation, PWA-Funktionen, automatische Tests und Deployment sind noch offen und werden in späteren Projektphasen ergänzt.



## 1. Projektübersicht

Dieses Projekt ist eine Messenger-App mit Microservices-Architektur.

Aktueller Backend-Stand:

- Auth Service
- User Service
- Shared Auth/JWT Utilities
- PostgreSQL-Datenbanken
- FastAPI API-Endpunkte
- JWT-basierte Authentifizierung

Noch offen:

- Messaging Service
- WebSocket-Kommunikation
- React Frontend
- PWA-Funktionen
- Deployment
- Tests


---

## 2. Technologie-Stack

Backend:

- Python
- FastAPI
- Uvicorn
- SQLAlchemy async
- PostgreSQL
- Pydantic
- JWT mit python-jose
- Passwort-Hashing mit passlib und bcrypt

Frontend später:

- React
- Vite
- Axios
- React Router
- PWA

Entwicklungsumgebung:

- Windows mit WSL Ubuntu
- VS Code
- Git/GitHub

---

## 3. Projektstruktur

Aktuelle Struktur:

```text
messenger-app/
├── auth_service/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   ├── dependencies.py
│   │   ├── routes.py
│   │   └── create_tables.py
│   ├── venv/
│   ├── .env
│   ├── .env.example
│   └── requirements.txt
│
├── user_service/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── dependencies.py
│   │   ├── routes.py
│   │   └── create_tables.py
│   ├── venv/
│   ├── .env
│   ├── .env.example
│   └── requirements.txt
│
├── messaging_service/
├── shared/
│   ├── __init__.py
│   └── auth/
│       ├── __init__.py
│       └── jwt.py
│
├── frontend/
├── docs/
│   └── backend-progress.md
├── setup_project.sh
├── starter.sh
├── stop.sh

## 4. PostgreSQL-Datenbanken

Für die Microservice-Struktur wurden getrennte Datenbanken erstellt:

messenger_auth
messenger_user
messenger_messages

Zuordnung:

auth_service        → messenger_auth
user_service        → messenger_user
messaging_service   → messenger_messages

Jeder Service besitzt seine eigene Datenbank.

Der PostgreSQL-User für die lokale Entwicklung ist: postgres

Das lokale Entwicklungs-Passwort ist in den .env Dateien gespeichert und durch .gitignore geschützt.

## Passwort-Reset ohne E-Mail

Im Auth Service wurde ein Passwort-Reset-Flow ohne E-Mail-Versand ergänzt.  
Da diese Projektversion für Entwicklung und Abgabe gedacht ist, wird der Reset-Code aktuell direkt in der API-Response zurückgegeben. Dadurch kann der Flow vollständig über FastAPI Swagger UI getestet werden, ohne dass ein SMTP-Server oder E-Mail-Versand eingerichtet werden muss.

In einer produktiven Version sollte der Reset-Code nicht direkt in der Response stehen. Stattdessen müsste er über einen sicheren Kanal zugestellt werden, zum Beispiel per E-Mail, Push-Nachricht oder einen anderen verifizierten Kommunikationsweg.

### Ziel des Passwort-Reset-Flows

Der Passwort-Reset soll ermöglichen, dass ein Benutzer ein neues Passwort setzen kann, ohne eingeloggt zu sein.

Der Ablauf ist:

1. Der Benutzer fordert einen Reset-Code mit seiner E-Mail-Adresse an.
2. Das Backend prüft, ob ein Benutzer mit dieser E-Mail existiert.
3. Das Backend erstellt einen zufälligen sechsstelligen Reset-Code.
4. Der Reset-Code wird in der Datenbank gespeichert.
5. Für diese Entwicklungs-/Abgabeversion wird der Reset-Code direkt in der API-Response zurückgegeben.
6. Der Benutzer sendet E-Mail, Reset-Code und neues Passwort an den Confirm-Endpunkt.
7. Das Backend prüft, ob der Code existiert, zum richtigen Benutzer gehört, noch nicht benutzt wurde und nicht abgelaufen ist.
8. Das neue Passwort wird gehasht gespeichert.
9. Der Reset-Code wird als benutzt markiert.
10. Der Benutzer kann sich danach mit dem neuen Passwort einloggen.

---

## Neue Tabelle: `password_reset_codes`

Für den Passwort-Reset wurde im Auth Service ein neues SQLAlchemy-Modell erstellt:

```python
class PasswordResetCode(Base):
    __tablename__ = "password_reset_codes"