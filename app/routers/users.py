from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_current_superuser
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services import user_service
from app.tasks.email_tasks import send_welcome_email

router = APIRouter(prefix="/users", tags=["users"])


# Public: registration
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    if user_service.get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = user_service.create_user(db, data)
    send_welcome_email.delay(user.email, user.full_name)  # queued after commit
    return user


# Superuser only: list all users
@router.get("/", response_model=List[UserOut])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_superuser),
):
    return user_service.list_users(db, skip, limit)


# Logged-in user: own profile
@router.get("/me", response_model=UserOut)
def read_me(current: User = Depends(get_current_user)):
    return current


# Logged-in user: self or superuser
@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    if current.id != user_id and not current.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    if current.id != user_id and not current.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.update_user(db, user, data)


# Superuser only
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_superuser),
):
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.delete_user(db, user)