from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.profile import Profile
from app.services.supabase_service import supabase


security = HTTPBearer(auto_error=False)


def get_current_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Profile:
  if credentials is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="No se envió token de autenticación."
    )

  if credentials.scheme.lower() != "bearer":
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Formato de autenticación inválido."
    )

  token = credentials.credentials

  try:
      response = supabase.auth.get_user(token)
      user = response.user
  except Exception:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token inválido o expirado."
    )

  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Usuario no autenticado."
    )

  try:
      user_id = UUID(user.id)
  except ValueError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="ID de usuario inválido."
    )

  profile = db.query(Profile).filter(Profile.id == user_id).first()

  if profile is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="No existe un perfil asociado a este usuario."
    )

  return profile