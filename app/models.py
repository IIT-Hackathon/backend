from .database import Base
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

class User(Base) :
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Integer, nullable=False)
    bookings = relationship("Booking", back_populates="user")
    
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String(20), nullable=False)
    service_type = Column(String(20), nullable=True)
    status = Column(Integer, nullable=False)
    user = relationship("User", back_populates="bookings")
    
class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, nullable=False)
    photo = Column(String(300), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(300), nullable=True)
    category = Column(String(50), nullable=False)