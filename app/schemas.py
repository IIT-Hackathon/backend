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
    
class TaxInfoResponse(BaseModel) :
    income : int
    city : str
    
class UpdateUser(BaseModel) :
    name : str
    age : int
    gender : str
    city : str
        
class ResponseUser(BaseModel) :
    name : str
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
    id : int 
    email : str

class TokenResponse(BaseModel) :
    access_token : str
    token_type : str
    id : int 
    role : int 
    phone : str 
    name : str
    email : str
    
    class Config :
        orm_mode = True