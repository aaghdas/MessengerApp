from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router as auth_router


# FastAPI-Anwendung für den Auth Service.
app = FastAPI(title="Auth Service")


# CORS-Konfiguration für lokale Entwicklung.
# Dadurch darf das React-Frontend später Anfragen an diesen Service senden.
#CORS wird gebraucht, damit React-Frontend auf den Auth Service zugreifen darf.
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


# Auth-Router wird in die FastAPI-Anwendung eingebunden.
# Dadurch werden Endpunkte wie /auth/register, /auth/login
# und /auth/current-user verfügbar.
app.include_router(auth_router)


# Einfacher Health-Check-Endpunkt.
# Damit kann geprüft werden, ob der Auth Service läuft.
@app.get("/")
def root():
    return {
        "service": "auth_service",
        "status": "running"
    }

"""
add_middleware bedeutet: FastAPI bekommt eine zusätzliche Zwischenschicht, die jede Anfrage und Antwort mitverarbeitet.

In diesem Fall fügen wir CORS-Middleware hinzu.
app.add_middleware(
    CORSMiddleware,
    ...)
Wenn React-Frontend z. B. auf http://127.0.0.1:5173 und Auth Service auf http://127.0.0.1:8001 läufen:
Das sind für den Browser zwei verschiedene Origins/Adressen. Ohne CORS kann der Browser Anfragen vom Frontend an Backend blockieren.
Mit:
allow_origins=[
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]
Anfragen vom React-Frontend auf Port 5173 sind erlaubt.
app.add_middleware(CORSMiddleware, ...) heißt:
FastAPI soll CORS-Regeln benutzen, damit das React-Frontend später mit dem Backend sprechen

"""