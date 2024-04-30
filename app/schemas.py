from pydantic import BaseModel, EmailStr


class User(BaseModel) :
    username : str
    email : EmailStr
    password : str
    role : int
    
class Photo(BaseModel) :
    photo : str
    title : str
    description : str
    category : str
     
class ResponseUser(BaseModel) :
    id : int
    username : str
    email : EmailStr
    role : int 

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
    user : ResponseUser
    
    class Config :
        orm_mode = True