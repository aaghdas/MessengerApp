# Gemeinsame JWT-Hilfsfunktionen für mehrere Backend-Services.
#
# Diese Datei enthält Funktionen zum Prüfen und Auslesen von JWT Access Tokens.
# Der Code liegt im shared-Bereich, damit Services wie user_service und
# messaging_service dieselbe Token-Logik verwenden können.
#
# Die Token-Erstellung bleibt im Auth Service.
# Andere Services prüfen nur, ob ein Token gültig ist und welche Benutzer-ID
# im Token enthalten ist.

from jose import JWTError, jwt


# Prüft ein JWT Access Token und gibt die Benutzer-ID zurück.
# Bei ungültigem, abgelaufenem oder fehlerhaftem Token wird None zurückgegeben.
def decode_access_token(
    token: str,
    secret_key: str,
    algorithm: str,
) -> int | None:
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm],
        )

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except (JWTError, ValueError):
        return None
        