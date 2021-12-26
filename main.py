import coloredlogs, logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.db_api.postgres import Database

from peerspace_scraper.scraper import Peerspace
from splacer_scraper.scraper import Splacer


if __name__ == '__main__':
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    coloredlogs.install()
    logging.basicConfig(level=logging.INFO)

    db = Database()

    peerspace = Peerspace(driver, db)
    peerspace.start()

    # splacer = Splacer(driver, db)
    # splacer.start()

    time.sleep(10)
