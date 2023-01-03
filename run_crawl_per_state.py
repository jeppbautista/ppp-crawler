from ppp_crawler.crawler import Crawler

from selenium.webdriver.common.by import By
import time

start_time = time.time()
crawler = Crawler()
loans = crawler.get_ppp_loans()

for loan in loans:
    loan_detail = crawler.get_loan_detail(loan)
    loan_detail.save()

print("--- %s seconds ---" % (time.time() - start_time))