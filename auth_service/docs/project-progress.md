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