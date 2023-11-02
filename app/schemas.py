from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class User(BaseModel) :
    name : str
    email : EmailStr
    password : str
    dob : date
    gender : str
    city : str
    
class Tax(BaseModel) :
    year : int
    income : int
    city : str
    
class UpdateUser(BaseModel) :
    name : str
    phone : str
    password : str
        
class ResponseUser(BaseModel) :
    id : int
    name : str
    email : str
    age : int
    gender : str
    city : str

    class Config :
        orm_mode = True
        
class UserLogin(BaseModel) :
    username : EmailStr
    password : str

class Token(BaseModel) :
    access_token : str
    token_type : str

class TokenData(BaseModel) :
    id : int | None = None
    email : str | None = None

class TokenResponse(BaseModel) :
    access_token : str
    token_type : str
    id : int | None = None
    role : int | None = None
    phone : str | None = None
    name : str | None = None
    email : str | None = None
    
    class Config :
        orm_mode = True