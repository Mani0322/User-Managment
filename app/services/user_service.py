from typing import Any,Optional,List
from sqlalchemy.orm import Session
from app.core.security import get_password_hash,verify_password
from app.models.user import User
from app.schemas.user import UserCreate,UserUpdate

def get_user(db:Session,user_id:int)->Optional[User]:
    return db.query(User).filter(User.id==user_id).first()

def get_user_by_email(db:Session,email:str)->Optional[User]:
    return db.query(User).filter(User.email==email).first()


def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db:Session,data:UserCreate)->User:
    user = User(
        full_name=data.full_name,
        email=data.email,
        hashed_password=get_password_hash(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def update_user(db:Session,user:User,data:UserUpdate)->User:
    changes = data.model_dump(exclude_unset=True)
    if "password" in changes:
        user.hashed_password = get_password_hash(changes.pop("password"))
    for field,value in changes.items():
        setattr(user,field,value)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()