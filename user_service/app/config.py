from pydantic_settings import BaseSettings, SettingsConfigDict


from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Absoluter Pfad zur .env Datei des User Service.
# Dadurch wird die Datei korrekt gefunden, egal aus welchem Ordner der Service gestartet wird.
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


# Diese Klasse enthält alle Einstellungen,
# die vom User Service aus der .env Datei benötigt werden.
class Settings(BaseSettings):
    # Verbindung zur PostgreSQL-Datenbank.
    # Der echte Wert wird aus user_service/.env geladen.
    DATABASE_URL: str

    # Geheimer Schlüssel zum Prüfen von JWT-Tokens.
    # Dieser Wert muss mit dem JWT_SECRET_KEY im Auth Service übereinstimmen.
    JWT_SECRET_KEY: str

    # Algorithmus zur JWT-Prüfung.
    # Dieser Wert muss ebenfalls mit dem Auth Service übereinstimmen.
    JWT_ALGORITHM: str = "HS256"

    # Pydantic-Konfiguration.
    # Die .env Datei wird über einen absoluten Pfad geladen.
    model_config = SettingsConfigDict(env_file=ENV_FILE)


# Zentrale Settings-Instanz für den User Service.
settings = Settings()