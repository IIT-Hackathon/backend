from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) :
    return pwd_context.verify(plain_password, hashed_password)

def calculate_income_tax(gender, age, city, income):
    male_threshold = 350000
    female_threshold = 400000
    senior_citizen_threshold = 400000
    dhaka_chattogram_tax = 5000
    other_city_tax = 4000
    non_city_tax = 3000

    if gender == "male":
        threshold = male_threshold
    elif gender == "female" or age > 65:
        threshold = female_threshold
    else:
        threshold = male_threshold
        
    taxable_income = max(income - threshold, 0)

    tax = 0
    if taxable_income <= 100000:
        tax = taxable_income * 0.05
    elif taxable_income <= 400000:
        tax = 100000 * 0.05 + (taxable_income - 100000) * 0.1
    elif taxable_income <= 800000:
        tax = 100000 * 0.05 + 300000 * 0.1 + (taxable_income - 400000) * 0.15
    elif taxable_income <= 1300000:
        tax = 100000 * 0.05 + 300000 * 0.1 + 400000 * 0.15 + (taxable_income - 800000) * 0.20
    else:
        tax = 100000 * 0.05 + 300000 * 0.1 + 400000 * 0.15 + 500000 * 0.20 + (taxable_income - 1300000) * 0.25


    if city == "dhaka" or city == "Chattogram":
        tax = max(tax, dhaka_chattogram_tax)
    elif city == "other city":
        tax = max(tax, other_city_tax)
    else:
        tax = max(tax, non_city_tax)

    return tax

def calculate_age(dob) :
    current_time = datetime.now()
    age = current_time.year - dob.year - ((current_time.month, current_time.day) < (dob.month, dob.day))
    return age