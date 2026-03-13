from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file create hogi
SQLALCHEMY_DATABASE_URL = "sqlite:///./admin_system.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database session handle karne ke liye function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()