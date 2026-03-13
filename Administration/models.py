from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class AdminUser(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

class SystemResource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String, default="Online")