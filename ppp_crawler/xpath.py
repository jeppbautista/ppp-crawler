class Root:
    ROOT = "/html/body"
    
class State(Root):
    STATES = "./div/div/table/tbody/tr/td[1]"
    _RAW_NAME = "./a"
    _LINK = "./a"
    
class City(Root):
    CITIES = "./div/div/div/div[2]/table/tbody/tr/td[1]"
    _RAW_NAME = "./a"
    _LINK = "./a"
    
class Loan(Root):
    LOANS = "./div/div/div/div[2]/table/tbody/tr[1]/td[2]"
    _BUSINESS_NAME = "./a/b"
    _LINK = "./a"
    
class LoanDetail(Root):
    TABLE = "./div/div/div/div[2]/table"
    _ADDRESS = """//td[text()="Address"]/following-sibling::td"""
    _JOBS_RETAINED = """//td[text()="Jobs Retained"]/following-sibling::td"""
    _DATE_APPROVED = """//td[text()="Date Approved"]/following-sibling::td"""