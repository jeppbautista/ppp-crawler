from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import os
from ppp_crawler.config import Config
from ppp_crawler.driver import Driver
from ppp_crawler import xpath
from ppp_crawler.entities import City, Loan, State


class Crawler:
    def __init__(self, driver_options:list = None) -> None:
        
        options = driver_options if isinstance(driver_options, list) else []
        self.driver = Driver(*options).get_driver()
        self.root = self.__get_root(Config.CRAWL_ROOT_URL)
    
    def get_ppp_loans(self) -> None:
        
        states = self.__get_states()[1:2]
        cities = [self.__get_cities(state) for state in states]
        
        cities = [i for city in cities for i in city][1:4]
        
        loans = [self.__get_loans(city) for city in cities]
        loans = [i for loan in loans for i in loan]
        return loans 
    
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
    
        
        
        
        
        
    
    
    
    