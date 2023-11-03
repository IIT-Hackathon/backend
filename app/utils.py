from passlib.context import CryptContext
from datetime import datetime

male_threshold = 350000
female_threshold = 400000
senior_citizen_threshold = 400000

dhaka_chattogram_tax = 5000
other_city_tax = 4000
non_city_tax = 3000

tax_brackets = [
    {
        "limit": 100000,
        "rate": 0.05
    },
    {
        "limit": 300000,
        "rate": 0.1
    },
    {
        "limit": 400000,
        "rate": 0.15
    },
    {
        "limit": 500000,
        "rate": 0.2
    },
]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) :
    return pwd_context.verify(plain_password, hashed_password)

def calculate_income_tax(gender, age, city, income):
    
    
    breakdown = []

    if gender == "female" or age > 65:
        threshold = female_threshold
    else:
        threshold = male_threshold
        
        
    taxable_income = max(income - threshold, 0)
    total_taxable_income = taxable_income
    tax = 0
    
    for bracket in tax_brackets:
        to_tax_on = min(taxable_income, bracket["limit"])
        tax = to_tax_on * bracket["rate"]
        taxable_income -= to_tax_on
        breakdown.append({
            "message": f"{bracket['rate'] * 100}% tax on next {bracket['limit']} bracket.",
            "amount": tax
        })
    
    
    if taxable_income > 0:
        tax = taxable_income * 0.25
        breakdown.append({
            "message": f"25% tax on remaining amount.",
            "amount": tax
        })
    
    tax = sum([bracket["amount"] for bracket in breakdown])
    

    if taxable_income > 0 and  (city == "dhaka" or city == "Chattogram"):
        
        if tax < dhaka_chattogram_tax:
            tax = dhaka_chattogram_tax
            breakdown.append({
                "message": f"Minimum tax for Dhaka/Chattogram.",
                "amount": tax
            })
        
        # tax = max(tax, dhaka_chattogram_tax)
    elif taxable_income > 0 and  city == "other city":
        # tax = max(tax, other_city_tax)
        if tax < other_city_tax:
            tax = other_city_tax
            breakdown.append({
                "message": f"Minimum tax for city corporation.",
                "amount": tax
            })
    elif taxable_income > 0 and  city == "non city":
        
        # tax = max(tax, non_city_tax)
        if tax < non_city_tax:
            tax = non_city_tax
            breakdown.append({
                "message": f"Minimum tax for non city corporation.",
                "amount": tax
            })

    return tax, breakdown, total_taxable_income

def calculate_age(dob) :
    current_time = datetime.now()
    age = current_time.year - dob.year - ((current_time.month, current_time.day) < (dob.month, dob.day))
    return age