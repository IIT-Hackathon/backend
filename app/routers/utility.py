from fastapi import FastAPI, Response, HTTPException, Depends, APIRouter, Query
from fastapi.params import Body
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import User, ResponseUser, UpdateUser, Token, TokenResponse
from passlib.context import CryptContext
from typing import List
from .. import models, oauth2


router = APIRouter()

district_names = [
    "Barguna",
    "Barisal",
    "Bhola",
    "Jhalokati",
    "Patuakhali",
    "Pirojpur",
    "Bandarban",
    "Khagrachhari",
    "Rangamati",
    "Bagerhat",
    "Chuadanga",
    "Jessore",
    "Jhenaidah",
    "Khulna",
    "Kushtia",
    "Magura",
    "Meherpur",
    "Narail",
    "Satkhira",
    "Bogra",
    "Joypurhat",
    "Naogaon",
    "Natore",
    "Pabna",
    "Rajshahi",
    "Sirajganj",
    "Brahmanbaria",
    "Chandpur",
    "Comilla",
    "Feni",
    "Khagrachhari",
    "Lakshmipur",
    "Noakhali",
    "Rangamati",
    "Cox's Bazar",
    "Faridpur",
    "Gopalganj",
    "Madaripur",
    "Manikganj",
    "Munshiganj",
    "Narayanganj",
    "Shariatpur",
    "Dhaka",
    "Gazipur",
    "Kishoreganj",
    "Manikganj",
    "Munshiganj",
    "Narayanganj",
    "Narsingdi",
    "Rajbari",
    "Tangail",
    "Dinajpur",
    "Gaibandha",
    "Kurigram",
    "Lalmonirhat",
    "Nilphamari",
    "Panchagarh",
    "Rangpur",
    "Thakurgaon",
    "Habiganj",
    "Moulvibazar",
    "Sunamganj",
    "Sylhet",
]

@router.get("/cities", status_code = 200, tags=["utils"]) 
def get_cities() :
    lowercase_district_names = [name.lower() for name in district_names]
    return {"cities" : lowercase_district_names}


@router.get("/genders", status_code = 200, tags=["utils"])
def get_genders() :
    return {"genders" : ["male", "female"]}