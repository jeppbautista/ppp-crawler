from selenium.webdriver.remote.webelement import WebElement

from abc import ABC, abstractmethod

class Loans:
    loan_amount_range: str
    loan_amount_min: float
    loan_amount_max: float
    business_name: str
    address: str
    naics_code: str
    business_type: str
    race: str
    gender: str
    veteran: str
    jobs_retained: str
    date_approved: str
    lender: str
    state: str
    city: str
    cd: str
    status: str
    is_extracted: bool = False
    element: WebElement
    
    
    