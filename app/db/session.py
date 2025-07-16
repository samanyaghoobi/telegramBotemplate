from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

_engine = create_engine(settings.dsn, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)

def get_session():
    return SessionLocal()

engine = _engine