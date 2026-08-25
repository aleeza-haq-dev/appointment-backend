import os
import datetime as dt
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./appointments_db.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Appointment(Base):
    _tablename_ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, index=True)
    reason = Column(String, nullable=True)
    start_time = Column(DateTime, index=True)
    canceled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

def get_db():
     db: Session = SessionLocal()
     try:
          yield db
     finally:
          db.close()

if _name=="main_":
        init_db()
