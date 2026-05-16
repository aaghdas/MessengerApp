from pydantic_settings import BaseSettings, SettingsConfigDict


# Diese Klasse enthält alle Einstellungen,
# die vom User Service aus der .env Datei benötigt werden.
class Settings(BaseSettings):
    # Verbindung zur PostgreSQL-Datenbank.
    # Der echte Wert wird aus user_service/.env geladen.
    #
    # Beispiel:
    # postgresql+asyncpg://postgres:messenger_dev_123@localhost:5432/messenger_user
    DATABASE_URL: str

    # model_config ist ein spezieller Pydantic-v2-Name, der nicht geändert werden sollte.
    #
    # Diese Zeile legt fest:
    # Die Werte für diese Settings-Klasse werden aus der Datei ".env" gelesen.
    model_config = SettingsConfigDict(env_file=".env")


# Hier wird ein Settings-Objekt erstellt.
# Beim Erstellen wird die .env Datei automatisch gelesen.
#
# Andere Dateien können später importieren:
# from app.config import settings
#
# Dadurch können z. B. folgende Werte verwendet werden:
# settings.DATABASE_URL
settings = Settings()