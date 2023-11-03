from .database import Base
from sqlalchemy import Integer, Boolean, String, Column, ForeignKey, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User(Base) :
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=True)
    dob = Column(TIMESTAMP(timezone=True), nullable=False)
    gender = Column(String, nullable=False)
    city = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
class Tax(Base) :
    __tablename__ = "tax_reports"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    year = Column(Integer, nullable=False)
    income = Column(Integer, nullable=False)
    taxable_income = Column(Integer, nullable=False)
    tax = Column(Float, nullable=False)
    city = Column(String, nullable=False)
    breakdown = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
    


