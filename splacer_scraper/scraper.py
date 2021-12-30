import logging
import time
import datetime
import requests

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class Splacer:
    def __init__(self, driver, db):
        self.driver = driver
        self.db = db

    def parse_activities(self):
        """
        This method parses activities from target website: peerspace.com,
        to form a search query for each activity in future and group parsed items based on this in monthly report

        returns a list of parsed activities
        """

        # redirecting to activities page

        logging.info('[ SPLACER ]: Activity parsing started')

        self.driver.get('https://www.splacer.co/search/activities')

        # finding the container div of available activities on the page

        activities_container = self.driver.find_element(By.CLASS_NAME, 'seo-list')

        # finding all activity categories

        categories = activities_container.find_elements(By.CLASS_NAME, 'category')

        result = dict()

        for category in categories:
            category_name = category.find_element(By.TAG_NAME, 'h3').text
            activities = category.find_elements(By.TAG_NAME, 'a')
            category_activities = []

            for activity in activities:
                category_activities.append(activity.text)

            result[str(category_name)] = list(category_activities)

        return result

    def parse_locations(self):
        """
        This method parses locations from target website: peerspace.com,
        to form a search query for each activity in future and group parsed items based on this in monthly report

        returns a list of parsed locations
        """
        # redirecting to locations page

        logging.info('[ SPLACER ]: Locations parsing started')

        self.driver.get('https://www.splacer.co/rent/locations')

        # finding the container div of available locations on the page

        locations_container = self.driver.find_element(By.CLASS_NAME, 'page-section-inner')

        # finding all locations links

        locations_links = locations_container.find_elements(By.TAG_NAME, 'a')

        result = []

        for location in locations_links:
            result.append(location.text)

        logging.info('[ SPLACER ]: Locations parsing finished')
        return result

    def start(self):
        """
        Generates get requests to parse items with
        Example of the url:
        https://www.splacer.co/splaces/search?activity_category=Corporate%20Event&city=New%20York&activity=Business%20Brunch&sort_by=popularity
        """
        activities = self.parse_activities()
        locations = self.parse_locations()

        for location in locations[16:]:
            for key in activities:
                for activity in activities[key]:
                    print(location + " : " + key + " : " + activity)
                    url = 'https://www.splacer.co/splaces/search?activity_category=' + str(key) + '&city=' + str(
                        location) + '&activity=' + str(activity) + '&sort_by=popularity'
                    self.proceed_url(url)

    def parse_page(self, links_list):
        """
        This method parses given page and updates rows in database,
        to form a report in future
        """

        for link in links_list:
            page = requests.get(link)
            soup = BeautifulSoup(page.text, 'html.parser')

            # parsing data
            location_name = soup.find('div', class_='title').text.translate(''.join(["'", '"']))
            try:
                host_name = soup.find('div', class_='owner-name').text.translate(''.join(["'", '"']))
            except AttributeError:
                host_name = None
            try:
                listing_location = soup.find('span', class_='splace-city').text.translate(''.join(["'", '"']))
            except:
                listing_location = None
            try:
                container = soup.find('div', class_='h-stars')
                reviews_count = container.find('div', class_='sp-pointer').text
                reviews_count = ''.join(c for c in str(reviews_count) if c.isdigit())
            except Exception as e:
                reviews_count = 0

            # there is no access to phone number on the page
            phone_number = None

            try:
                self.db.add_listing('splacer', link, location_name, host_name, listing_location, phone_number,
                                    int(reviews_count), datetime.datetime.now())
            except Exception as e:
                print(e)

            print(link)
            print(location_name)
            print(host_name)
            print(listing_location)
            print(reviews_count)
            print(phone_number)
            print('\n\n\n\n')

    def proceed_url(self, url):
        logging.info('[ SPLACER ]: Processing url: ' + url)

        self.driver.get(url)

        # checking if page has pagination buttons
        try:
            pagination_ul = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.pagination')))

            logging.warning('[ SPLACER ]: Pagination found')

            while True:

                time.sleep(1)
                links = []

                try:
                    cards = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'sp-splace')))

                    for card in cards:
                        try:

                            # to skip sponsored links

                            link = card.find_element(By.CLASS_NAME, 'sp-title').get_attribute('href')
                            print(link)
                            links.append(link)
                        except Exception as e:
                            print(e)

                except TimeoutException:
                    pass

                self.parse_page(links)

                # trying to go to the next pagination page
                try:
                    pagination_elems = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))

                    for pag in pagination_elems:
                        if pag.get_attribute(
                                'innerHTML') == '<a role="button" href="#"><span aria-label="Next">›</span></a>':
                            actions = ActionChains(self.driver)
                            actions.move_to_element(pag).perform()
                            pag.find_element(By.TAG_NAME, 'a').click()

                        elif pag.get_attribute(
                                'innerHTML') == '<a role="button" href="#" tabindex="-1" style="pointer-events: none;"><span aria-label="Next">›</span></a>':
                            logging.warning('Pagination parsing finished')
                            break

                except ElementClickInterceptedException:
                    logging.warning('Pagination parsing finished')
                    break

        except TimeoutException:
            logging.info('[ SPLACER ]: Pagination not found')

            links_list = []

            try:
                items_container = self.driver.find_element(By.CLASS_NAME, 'search-thumbnails')
                items = items_container.find_elements(By.CLASS_NAME, 'Listing-Thumbnail')

                for item in items:
                    links_list.append(item.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            except:
                # if page is emtpy
                logging.info('[ SPLACER ]: Page is empty')

            self.parse_page(links_list)
