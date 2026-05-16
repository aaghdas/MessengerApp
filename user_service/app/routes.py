# API-Routen für den User Service.
# Diese Datei definiert die Endpunkte für Benutzerprofile und Kontakte.
# Hier werden eingehende API-Anfragen verarbeitet, Daten über SQLAlchemy
# aus der PostgreSQL-Datenbank gelesen oder gespeichert und passende
# API-Antworten zurückgegeben.
# Die Datei enthält keine Datenbankmodelle und keine zentrale Konfiguration.
# Models liegen in models.py, Schemas in schemas.py und die Datenbankverbindung in database.py.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Contact, Profile
from app.schemas import (
    ContactCreate,
    ContactResponse,
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)


# Router für alle User-Service-Endpunkte.
# Hier werden Profil- und Kontakt-Routen gesammelt.
router = APIRouter(tags=["User Service"])


# Erstellt ein neues Benutzerprofil.
@router.post(
    "/profiles",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    profile_data: ProfileCreate,
    db: AsyncSession = Depends(get_db),
):
    existing_profile_result = await db.execute(
        select(Profile).where(Profile.auth_user_id == profile_data.auth_user_id)
    )
    existing_profile = existing_profile_result.scalar_one_or_none()

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user.",
        )

    new_profile = Profile(
        auth_user_id=profile_data.auth_user_id,
        display_name=profile_data.display_name,
        bio=profile_data.bio,
        avatar_url=profile_data.avatar_url,
    )

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    return new_profile


# Gibt ein Profil anhand der Auth-User-ID zurück.
@router.get("/profiles/{auth_user_id}", response_model=ProfileResponse)
async def get_profile(
    auth_user_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Profile).where(Profile.auth_user_id == auth_user_id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )

    return profile


# Aktualisiert ein bestehendes Profil.
@router.put("/profiles/{auth_user_id}", response_model=ProfileResponse)
async def update_profile(
    auth_user_id: int,
    profile_data: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Profile).where(Profile.auth_user_id == auth_user_id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )

    update_data = profile_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(profile, field, value)

    await db.commit()
    await db.refresh(profile)

    return profile


# Erstellt einen neuen Kontakt.
@router.post(
    "/contacts",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    contact_data: ContactCreate,
    db: AsyncSession = Depends(get_db),
):
    if contact_data.owner_user_id == contact_data.contact_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user cannot add themselves as a contact.",
        )

    new_contact = Contact(
        owner_user_id=contact_data.owner_user_id,
        contact_user_id=contact_data.contact_user_id,
    )

    db.add(new_contact)

    try:
        await db.commit()
        await db.refresh(new_contact)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contact already exists.",
        )

    return new_contact


# Gibt alle Kontakte eines Benutzers zurück.
@router.get("/contacts/{owner_user_id}", response_model=list[ContactResponse])
async def get_contacts(
    owner_user_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contact).where(Contact.owner_user_id == owner_user_id)
    )
    contacts = result.scalars().all()

    return contacts


# Löscht einen Kontakt anhand seiner Kontakt-ID.
@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Contact).where(Contact.id == contact_id)
    )
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found.",
        )

    await db.delete(contact)
    await db.commit()

    return None