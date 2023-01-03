from selenium.webdriver.remote.webelement import WebElement

from abc import ABC, abstractmethod
import csv
from dataclasses import dataclass
import datetime
import json
import os
import shutil

@dataclass
class State:
    raw_name: str
    link: str
    element: WebElement
    name: str = None
    code: str = None
    
    def __post_init__(self):
        self.code = self.raw_name.split("-")[0].strip().upper()
        self.name = self.raw_name.split("-")[-1].strip().upper()
    
    def __repr__(self):
        return f"State(raw_name={self.raw_name}, code={self.code}, name={self.name})"
    
    def save(self, path:str = "./"):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        path = os.path.join(path, "state\\", current_date)
        if not os.path.exists(path):
            os.makedirs(path)
            
        print(os.path.join(path, f"{self.raw_name}.json"))
        with open(os.path.join(path, f"{self.raw_name}.json"), "w+") as file:
            json.dump(self.to_dict(), file)
        
    def to_dict(self):
        return dict(
            raw_name=self.raw_name,
            link=self.link,
            name=self.name,
            code=self.code,
            element=self.element.get_attribute("innerHTML")
        )
    
@dataclass
class City:
    raw_name: str
    link: str
    state: State
    element: WebElement
    name: str = None
    
    def __post_init__(self):
        self.name = self.raw_name.strip()
    
    def __repr__(self):
        return f"City(raw_name={self.raw_name}, state={self.state})"

@dataclass
class Loan:
    business_name: str
    link: str
    city: City
    element: WebElement
    
    def __post_init__(self):
        self.business_name = self.business_name.strip()
    
    def __repr__(self) -> str:
        return f"Loan(business_name={self.business_name}, city={self.city})"
    
@dataclass
class LoanDetail(Loan):
    address: str
    jobs_retained: str
    date_approved: str
    status: str
    element: WebElement
    is_extracted: bool = False
    
    def __repr__(self) -> str:
        return f"Loan(business_name={self.business_name}, LoanDetail(address={self.address}, jobs_retained={self.jobs_retained}, date_approved={self.date_approved}))"
    
    def save(self, path:str="./output"):
        path = os.path.join(path, f"{self.city.state.name}.csv")
            
        with open(path, 'a+', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["state", "city", "business_name", "address", "jobs_retained", "date_approved"])
            writer.writerow(self.to_dict())
    
    def to_dict(self):
        return dict(
            state=self.city.state.name,
            city=self.city.name,
            business_name=self.business_name,
            address=self.address,
            jobs_retained=self.jobs_retained,
            date_approved=self.date_approved
        )
    