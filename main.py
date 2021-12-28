import datetime
import time

import coloredlogs
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from peerspace_scraper.scraper import Peerspace
from utils.db_api.postgres import Database
from utils.notifications.reporter import Reporter

if __name__ == '__main__':
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    coloredlogs.install()
    logging.basicConfig(level=logging.INFO)

    db = Database()

    PARSING_STARTED = datetime.datetime.now()

    # peerspace = Peerspace(driver, db)
    # peerspace.start()

    # splacer = Splacer(driver, db)
    # splacer.start()

    PARSING_FINISHED = datetime.datetime.now()

    reporter = Reporter(db, PARSING_STARTED, PARSING_FINISHED)
    reporter.parse_tables()

    time.sleep(10)
