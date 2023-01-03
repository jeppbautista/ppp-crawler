from ppp_crawler.crawler import Crawler

from selenium.webdriver.common.by import By

crawler = Crawler()
loans = crawler.get_ppp_loans()
for loan in loans:
    loan_detail = crawler.get_loan_detail(loan)
    loan_detail.save()
