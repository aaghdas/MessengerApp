from pydantic_settings import BaseSettings, SettingsConfigDict


# Diese Klasse enthält alle Einstellungen,
# die vom Auth Service aus der .env Datei benötigt werden.
class Settings(BaseSettings):
    # Verbindung zur PostgreSQL-Datenbank.
    # Der echte Wert wird aus auth_service/.env geladen.
    #
    # Beispiel:
    # postgresql+asyncpg://postgres:password@localhost:5432/messenger_auth
    DATABASE_URL: str

    # Geheimer Schlüssel für JWT-Tokens.
    # Damit werden Login-Tokens signiert und später geprüft.
    # Dieser Wert darf nicht öffentlich im code oder auf GitHub gespeichert werden.
    JWT_SECRET_KEY: str

    # Algorithmus für JWT.
    # HS256 ist ein üblicher Standard.
    # Falls in .env kein Wert gesetzt ist, wird "HS256" verwendet.
    JWT_ALGORITHM: str = "HS256"

    # Gültigkeitsdauer des Access Tokens in Minuten.
    # Falls in .env kein Wert gesetzt ist, wird 30 verwendet.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # model_config ist ein spezieller Pydantic-v2-Name. Der Name sollte nicht geändert werden.
    #
    # Diese Zeile legt fest: Die Werte für diese Settings-Klasse werden aus der Datei ".env" gelesen.
    model_config = SettingsConfigDict(env_file=".env")


# Hier wird ein Settings-Objekt erstellt.
# Beim Erstellen wird die .env Datei automatisch gelesen.
#
# Andere Dateien können später importieren:
# from app.config import settings
#
# Dadurch können z. B. folgende Werte verwendet werden:
# settings.DATABASE_URL
# settings.JWT_SECRET_KEY
settings = Settings()