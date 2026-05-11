from fastapi import FastAPI

from app.routes import router as auth_router


# FastAPI-Anwendung für den Auth Service.
app = FastAPI(title="Auth Service")


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