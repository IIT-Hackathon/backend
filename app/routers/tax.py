from fastapi import FastAPI, Depends, APIRouter, Query
from fastapi.params import Body
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import Tax, TaxInfoResponse
from typing import List
from .. import models, oauth2
from ..utils import calculate_income_tax, calculate_age
import json
from datetime import datetime

router = APIRouter( tags = ["Tax"] )


breakdown = {
    "Tax For The Initial 100,000 BDT (5 Percent)" : 5000,
    "Tax For The Next 300,000 BDT (10 Percent) " : 30000,
    "Tax For The Next 400,000 BDT (15 Percent) " : 40000,
    "Tax For The Next 500,000 BDT (20 Percent) " : 100000,
    "Additional 25% Tax For The Remaining Amount: ": "To Be Calculated",
    "Taxable Income" : 650000,
    "Total Tax" : 72500
}

city_corporations = [
    "dhaka",
    "chattogram",
    "khulna",
    "rajshahi",
    "barishal",
    "sylhet",
    "rangpur",
    "mymensingh",
    "gazipur",
    "narayanganj",
    "comilla"
]

@router.post("/new_tax", tags=['tax'])
def create_new_tax(tax : Tax, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    
    user_from_db = db.query(models.User).filter(models.User.id == user.id).first()
    age = calculate_age(user_from_db.dob)
    calculated_tax = calculate_income_tax(user_from_db.gender, age, tax.city, tax.income)
    taxable_income = max(tax.income - 350000, 0)
    breakdown_in_json = json.dumps(breakdown)
    if tax.city == 'dhaka' or tax.city == 'chattogram' :
        city = tax.city
    elif tax.city in city_corporations :
        city = 'other city'
    else :
        city = 'non city'  
    new_tax = models.Tax(year = tax.year, income = tax.income, taxable_income = taxable_income, city = city, tax = calculated_tax, user_id = user_from_db.id, breakdown=breakdown_in_json)
    db.add(new_tax)
    db.commit()
    db.refresh(new_tax)
    return new_tax 

@router.get("/reports", tags=['tax'])
def get_tax_reports(limit : int = 10, offset : int =  0, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    user_from_db = db.query(models.User).filter(models.User.id == user.id).first()
    tax_reports = db.query(models.Tax).filter(models.Tax.user_id == user_from_db.id).limit(limit=limit).offset(offset=offset).all()
    return tax_reports


@router.get("/current_report", tags=['tax'])
def get_tax_report(year : int, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    user_from_db = db.query(models.User).filter(models.User.id == user.id).first()
    tax_report = db.query(models.Tax).filter(models.Tax.user_id == user_from_db.id, models.Tax.year == year).first()
    return tax_report

@router.get("/tax_info", response_model = TaxInfoResponse, tags=['tax']) 
def get_tax_info(db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    user_from_db = db.query(models.User).filter(models.User.id == user.id).first()
    current_year = datetime.now().year
    tax_report = db.query(models.Tax).filter(models.Tax.user_id == user_from_db.id, models.Tax.year == current_year).first()
    if tax_report is None :
        return { "detail" : "error" }
    return tax_report

@router.put("/tax_info", tags=['tax']) 
def update_tax_info(tax_info : TaxInfoResponse, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    user_from_db = db.query(models.User).filter(models.User.id == user.id).first()
    current_year = datetime.now().year
    tax_report = db.query(models.Tax).filter(models.Tax.user_id == user_from_db.id, models.Tax.year == current_year).first()
    if tax_report is None :
        return { "detail" : "error" }
    tax_report.income = tax_info.income
    tax_report.city = tax_info.city
    if tax_info.city == 'dhaka' or tax_info.city == 'chattogram' :
        city = tax_info.city
    elif tax_info.city in city_corporations :
        city = 'other city'
    else :
        city = 'non city'
    calculated_tax = calculate_income_tax(user_from_db.gender, calculate_age(user_from_db.dob), city, tax_info.income)
    tax_report.tax = calculated_tax
    taxable_income = max(tax_info.income - 350000, 0)
    tax_report.taxable_income = taxable_income
    breakdown_in_json = json.dumps(breakdown)
    tax_report.breakdown = breakdown_in_json
    db.commit()
    db.refresh(tax_report)
    return tax_report
