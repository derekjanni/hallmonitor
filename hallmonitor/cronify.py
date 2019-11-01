import schedule
import time

def job(test_case, test):
    schedule.every().minute.do(test_case, **test)
    while True:
        schedule.run_pending()
