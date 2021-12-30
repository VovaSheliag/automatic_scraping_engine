import logging
import time
import datetime

import requests
from bs4 import BeautifulSoup

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class Partyslate:
    def __init__(self, driver, db):
        self.driver = driver
        self.db = db

    def parse_vendors(self):
        """
        This method parses vendors page and calls
        parse_vendor() method for each vendor to parse each vendor`s event
        """
        # detecting pagination length
        self.driver.get('https://www.partyslate.com/find-vendors')
        try:
            pag_container = self.driver.find_element(By.CLASS_NAME,
                                                     'components-Pagination-Pagination-module__container__3L4x4')
            logging.info('[ PARTYSLATE ]: Pagination found')
            pag_length = \
            pag_container.find_elements(By.CLASS_NAME, 'components-Pagination-Pagination-module__page__2wmsX')[-1].text
            logging.info('[ PARTYSLATE ]: Pagination length detected')
        except:
            logging.error('[ PARTYSLATE ]: Pagination not found. Something went wrong !!!')
            return 0

        # parsing pagination pages
        for pag in range(2, int(pag_length)):

            page_vendors = self.driver.find_elements(By.CLASS_NAME,
                                                     'components-FindCompaniesCard-FindCompaniesCard-module__container__C4nMu')

            for vendor in page_vendors:
                url = vendor.find_element(By.CLASS_NAME,
                                          'components-FindCompaniesCard-components-Header-Header-module__name__RZLR6').get_attribute(
                    'href')
                current_tab = self.driver.current_window_handle
                self.parse_vendor(url, current_tab)

            self.driver.get('https://www.partyslate.com/find-vendors?page=' + str(pag))
            logging.info('[ PARTYSLATE ]: Processing next pagination page')

    def parse_vendor(self, vendor_url, current_tab):
        """
        This method parses available events of each vendors
        """
        print(vendor_url)
        """logging.info('[ PARTYSLATE ]: Parsing vendor ' + str(vendor_url))

        self.driver.execute_script('''window.open("https://www.google.com", "_blank");''')
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.driver.get(vendor_url)

        time.sleep(2)

        while True:
            time.sleep(3)
            try:
                container = self.driver.find_element(By.CLASS_NAME,
                                                     'pages-profile-components-PaginatedGallery-styles__content__DoGzp')
                button = container.find_element(By.CLASS_NAME, 'components-Button-Button-module__text__3Ftmz')

                button.click()
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print('click')
                time.sleep(5)
            except:
                print('ecxept')
                break

        self.driver.close()
        self.driver.switch_to.window(current_tab)

        logging.info('[ PARTYSLATE ]: Parsing vendor finished')"""
