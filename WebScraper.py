# I'm going to refactor all webscraping code to classess for more readibility and easier use
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import facebook
from logins import facebook_api_login
from database import chceck_source

class WebScraper:
    concerts = []
    def __init__(self, url):
        self.url = url

    def scrape_data(self, specific_event_link=None, num_events=None, ALL=None):
        if "facebook" in self.url:
            return self.scrape_facebook_data()
        elif "rockmetal" in self.url:
            return self.scrape_rockmetal_data(specific_event_link, num_events, ALL)
        else:
            print("unknown website")
            return None

    def scrape_rockmetal_data(self, specific_event_link=None, num_events=None, ALL=None):
        if specific_event_link:
            response = requests.get(specific_event_link)
            soup = BeautifulSoup(response.content, "html.parser")
            concert_element = soup.find_all(class_="gigItemIn")
            concert_element = concert_element[0].get_text().splitlines()
            title = soup.find_all(class_="gigItemTitle")
            if title:
                data = [str(title[0])[25:-5]]
            else:
                data = [None]

            for element in concert_element:
                if element == "" or len(element) <= 2 and not "zł" in element:  # skip non-printable
                    continue
                data.append(element.strip())
            return data
        elif num_events:
            print(f"downloading {num_events} events")
            pass
        elif ALL:
            print("dowloading all events")
            response = requests.get("https://www.rockmetal.pl/koncerty.html")
            soup = BeautifulSoup(response.content, "html.parser")
            target_links = soup.find_all("a", text="szczegóły")
            links = []
            for link in target_links:
                links.append(link['href'])
            print(links)

            # TODO here scrape_specific

            pass
        else:
            print("please specify what to scrape")
            pass

    def scrape_facebook_data(self):
        pass


# Testing here
rockmetal_scraper = WebScraper("rockmetal")
#specific_event_data = rockmetal_scraper.scrape_data("https://www.rockmetal.pl/koncerty.html?koncert=56719_D_R_I_")
specific_event_data = rockmetal_scraper.scrape_data("https://www.rockmetal.pl/koncerty.html?koncert=56842_Summer_Discomfort")
print(specific_event_data)

scrape_ALL = rockmetal_scraper.scrape_data(ALL=True)
print(scrape_ALL)