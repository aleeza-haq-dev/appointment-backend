import datetime as dt
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import  Session, sessionmaker

DATABASE_URL = "sqlite:///./appointments_db.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 2.0 recommended way to define Base
# WITH THIS:
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, index=True)
    reason = Column(String, nullable=True)
    start_time = Column(DateTime, index=True)
    canceled = Column(Boolean, default=False)
    
    # Modern Python UTC timestamp (prevents deprecation warnings)
    created_at = Column(DateTime, default=lambda: dt.datetime.now(dt.timezone.utc))


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

def get_db():
     db: Session = SessionLocal()
     try:
          yield db
     finally:
          db.close()

if __name__=="__main__":
        init_db()