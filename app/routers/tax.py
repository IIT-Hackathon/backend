from fastapi import FastAPI, Response, HTTPException, Depends, APIRouter, Query
from fastapi.params import Body
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import Token, TokenResponse, Tax
from typing import List
from .. import models, oauth2
from ..utils import calculate_income_tax, calculate_age
import json

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

@router.post("/new_tax", tags=['tax'])
def create_new_tax(tax : Tax, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    
    user_from_db = db.query(models.User).filter(models.User.id == user.id).first()
    age = calculate_age(user_from_db.dob)
    calculated_tax = calculate_income_tax(user_from_db.gender, age, tax.city, tax.income)
    taxable_income = max(tax.income - 350000, 0)
    breakdown_in_json = json.dumps(breakdown)
    new_tax = models.Tax(year = tax.year, income = tax.income, taxable_income = taxable_income, city = tax.city, tax = calculated_tax, user_id = user_from_db.id, breakdown=breakdown_in_json)
    db.add(new_tax)
    db.commit()
    db.refresh(new_tax)
    return new_tax 