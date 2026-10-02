from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=True)

Base = declarative_base()

def get_db():
    """Dependency that yields a database session per HTTP request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()