import os
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Integer,
    String,
    JSON,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine

# ---------------------------------------------------------------------------
# Database URL handling – supports PostgreSQL (psycopg) and fallback SQLite
# ---------------------------------------------------------------------------
_raw_url = os.getenv(
    "DATABASE_URL",
    os.getenv("POSTGRES_URL", "sqlite:///./app.db")
)
# Fix common scheme mismatches
if _raw_url.startswith("postgresql+asyncpg://"):
    _raw_url = _raw_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif _raw_url.startswith("postgres://"):
    _raw_url = _raw_url.replace("postgres://", "postgresql+psycopg://")

# Add SSL args for remote Postgres (non‑localhost and not SQLite)
_connect_args: Dict[str, Any] = {}
if not _raw_url.startswith("sqlite") and "localhost" not in _raw_url:
    _connect_args["sslmode"] = "require"

engine = create_engine(_raw_url, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# ---------------------------------------------------------------------------
# Table name prefix – prevents collisions in shared DBs
# ---------------------------------------------------------------------------
TABLE_PREFIX = "studymate_164591_"  # StudyMate


class StudyPlan(Base):
    __tablename__ = f"{TABLE_PREFIX}study_plans"
    id = Column(String, primary_key=True, index=True)  # UUID string
    user_id = Column(String, nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    plan_data = Column(JSON, nullable=False)  # Raw AI‑generated payload
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationship to topics (embedded in plan_data, kept for future expansion)
    # topics = relationship("Topic", back_populates="study_plan")


class RevisionCard(Base):
    __tablename__ = f"{TABLE_PREFIX}revision_cards"
    id = Column(String, primary_key=True, index=True)  # UUID string
    user_id = Column(String, nullable=False, index=True)
    front = Column(Text, nullable=False)
    back = Column(Text, nullable=False)
    last_reviewed = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# ---------------------------------------------------------------------------
# Helper for FastAPI dependency injection
# ---------------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
