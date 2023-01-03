from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ppp_crawler.config import Config
from ppp_crawler.driver import Driver
from ppp_crawler import xpath


class Crawler:
    def __init__(self, driver_options:list = None) -> None:
        
        options = driver_options if isinstance(driver_options, list) else []
        self.driver = Driver(*options).get_driver()
        self.root = self.__get_root(Config.CRAWL_ROOT_URL)
    
    def get_ppp_loans(self) -> None:
        pass
    
    def __get_root(self, url:str) -> WebElement:
        self.driver.get(url)
        root = self.driver.find_element(By.XPATH, xpath.Root.ROOT)
        
        return root
    
    