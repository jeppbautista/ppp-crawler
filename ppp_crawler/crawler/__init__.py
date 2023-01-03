from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import logging
import os
from ppp_crawler.config import Config
from ppp_crawler.driver import Driver
from ppp_crawler import xpath
from ppp_crawler.entities import City, Loan, LoanDetail, State


class Crawler:
    def __init__(self, driver_options:list = None) -> None:
        
        options = driver_options if isinstance(driver_options, list) else []
        self.driver = Driver(*options).get_driver()
        self.root = self.__get_root(Config.CRAWL_ROOT_URL)
    
    def get_ppp_loans(self) -> None:
        states = self.__get_states()[1:2]
        cities = [self.__get_cities(state) for state in states]
        
        cities = [i for city in cities for i in city]
        
        loans = [self.__get_loans(city) for city in cities]
        loans = [i for loan in loans for i in loan]
        return loans 
    
    def get_loan_detail(self, loan:Loan):
        logging.info(f"Extracting loan detail from: {loan.link}")
        root = self.__get_root(loan.link)
        try:
            table = root.find_element(By.XPATH, xpath.LoanDetail.TABLE)
            loan_detail = LoanDetail(
                business_name=loan.business_name,
                link=loan.link,
                city=loan.city,
                address=table.find_element(By.XPATH, xpath.LoanDetail._ADDRESS).text,
                jobs_retained=table.find_element(By.XPATH, xpath.LoanDetail._JOBS_RETAINED).text,
                date_approved=table.find_element(By.XPATH, xpath.LoanDetail._DATE_APPROVED).text,
                status="SUCCESS",
                element=table,
                is_extracted=True
            )
        except NoSuchElementException as e:
            logging.error("No Such Element Exception")
            loan_detail = LoanDetail(
                business_name=loan.business_name,
                link=loan.link,
                city=loan.city,
                address=None,
                jobs_retained=None,
                date_approved=None,
                status="NoSuchElementException",
                element=None,
                is_extracted=False
            )
        
        return loan_detail
    
    def __get_root(self, url:str) -> WebElement:
        self.driver.get(url)
        root = self.driver.find_element(By.XPATH, xpath.Root.ROOT)
        
        return root
    
    def __get_states(self) -> list[State]:
        states = []
        raw_states = self.root.find_elements(By.XPATH, xpath.State.STATES)
        for state in raw_states:
            
            states.append(
                State(
                    raw_name = state.find_element(By.XPATH, xpath.State._RAW_NAME).text,
                    link = state.find_element(By.XPATH, xpath.State._LINK).get_attribute("href"),
                    element = state
                )
            )
            
        return states
    
    def __get_cities(self, state:State):
        logging.info(f"Extracting City from: {state.link}")
        root = self.__get_root(state.link)
        cities = []
        raw_cities = root.find_elements(By.XPATH, xpath.City.CITIES)
        
        for city in raw_cities:
            cities.append(
                City(
                    raw_name = city.find_element(By.XPATH, xpath.City._RAW_NAME).text,
                    link = city.find_element(By.XPATH, xpath.City._LINK).get_attribute("href"),
                    state = state,
                    element = city
                )
            )
            
        return cities
        
    def __get_loans(self, city:City):
        logging.info(f"Extracting Loans from: {city.link}")
        root = self.__get_root(city.link)
        loans = []
        raw_loans = root.find_elements(By.XPATH, xpath.Loan.LOANS)
        
        for loan in raw_loans:
            loans.append(
                Loan(
                    business_name=loan.find_element(By.XPATH, xpath.Loan._BUSINESS_NAME).text,
                    link=loan.find_element(By.XPATH, xpath.Loan._LINK).get_attribute("href"),
                    city=city,
                    element=loan
                )
            )
            
        return loans
    
        
        
        
        
        
    
    
    
    