# Haupteinstiegspunkt für den User Service.
#
# Diese Datei erstellt die FastAPI-Anwendung, bindet Middleware ein
# und registriert die API-Routen des User Service.
#
# Die eigentliche Profil- und Kontaktlogik liegt in routes.py.
# Die Datenbankverbindung liegt in database.py.
# Die Datenbankmodelle liegen in models.py.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router as user_router


# FastAPI-Anwendung für den User Service.
app = FastAPI(title="User Service")


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


# User-Router wird in die FastAPI-Anwendung eingebunden.
# Dadurch werden Profil- und Kontakt-Endpunkte verfügbar.
app.include_router(user_router)


# Einfacher Health-Check-Endpunkt.
# Damit kann geprüft werden, ob der User Service läuft.
@app.get("/")
def root():
    return {
        "service": "user_service",
        "status": "running"
    }