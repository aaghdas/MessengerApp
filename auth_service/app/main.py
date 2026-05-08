from fastapi import FastAPI

app = FastAPI(title="Auth Service")


@app.get("/")
def root():
    return {
        "service": "auth_service",
        "status": "running"
    }