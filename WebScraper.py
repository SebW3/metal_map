# I'm going to refactor all webscraping code to classess for more readibility and easier use
import time
import requests
from bs4 import BeautifulSoup
# from selenium import webdriver
# import re
# import facebook
# from logins import facebook_api_login
# from database import chceck_source

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
        # functions
        def f_specific_event_link(specific_event_link):
            print("downloading specific event data")
            response = requests.get(specific_event_link)
            soup = BeautifulSoup(response.content, "html.parser")
            concert_element = soup.find_all(class_="gigItemIn")

            concerts = []
            for element in concert_element:
                concert_element = element.get_text().splitlines()

                data = []
                title = soup.find_all(class_="gigItemTitle")
                if title:
                    title = str(title[0])[25:-5]
                else:
                    title = None
                bands_playing = []
                where = [None, None, None]  # place, club, address
                price = None
                added_date = None
                change_date = None
                when = None
                uwagi = None

                for element in concert_element:
                    if element == "" or len(element) <= 2 and not "zł" in element:  # skip non-printable
                        continue
                    data.append(element.strip())

                for i in range(len(data)):
                    if data[i] == "Wystąpi:":
                        bands_playing.append(data[i+1])
                    elif data[i] == "Wystąpią:":
                        j = 1
                        while ":" not in data[i+j]:
                            bands_playing.append(data[i+j])
                            j += 1
                    elif data[i] == "Kiedy:":
                        when = data[i+1]
                    elif data[i] == "Gdzie:":
                        for j in range(len(where)):
                            if ":" in data[i+j+1]:
                                break
                            where[j] = data[i+j+1]
                    elif data[i] == "Cena:":
                        price = data[i+1]
                    elif "Dodane:" in data[i]:
                        if "zmiana" in data[i]:
                            added_date = data[i].split(",")[0]
                            change_date = data[i].split(",")[1].strip()
                        else:
                            added_date = data[i]
                    elif data[i] == "Uwagi:":
                        uwagi = data[i+1]


                if "(www)" in bands_playing:
                    bands_playing.remove("(www)")

                print("+"*100)
                #print(data)
                print([title, bands_playing, when, where, price, added_date, change_date, uwagi])

                if len(concert_element) == 1:
                    return [title, bands_playing, when, where, price, added_date, change_date, uwagi]
                concerts.append([title, bands_playing, when, where, price, added_date, change_date, uwagi])

            return concerts

        def f_num_events(num_events):
            print(f"downloading {num_events} events")
            pass

        def f_ALL():
            print("dowloading all events")
            links = []
            i = 1
            while True:
                response = requests.get(f"https://www.rockmetal.pl/koncerty.html?view=1&page={i}")
                soup = BeautifulSoup(response.content, "html.parser")
                target_links = soup.find_all("a", text="szczegóły")

                for link in target_links:
                    links.append(link['href'])
                print(len(links), links)

                if soup.find_all(class_="pagerNext pagerFirstLast"):
                    print("last page reached")
                    break
                i += 1
                break  # working on smaller dataset for now

            data_ALL = []
            i = 0
            for link in links:
                print(link)
                data_ALL.append(f_specific_event_link(link))

                i += 1  # temp
                if i > 3:
                    break
                print("timer 1 sec")
                time.sleep(0.1)

            return data_ALL

        if specific_event_link:
            return f_specific_event_link(specific_event_link)
        elif num_events:
            return f_num_events(num_events)
        elif ALL:
            return f_ALL()
        else:
            print("please specify what to scrape")
            pass

    def scrape_facebook_data(self):
        pass


# Testing here
rockmetal_scraper = WebScraper("rockmetal")
#specific_event_data = rockmetal_scraper.scrape_data("https://www.rockmetal.pl/koncerty.html?koncert=56719_D_R_I_")
#specific_event_data = rockmetal_scraper.scrape_data("https://www.rockmetal.pl/koncerty.html?koncert=56842_Summer_Discomfort")
#print(specific_event_data)

scrape_ALL = rockmetal_scraper.scrape_data(ALL=True)
print("|"*100)
print(scrape_ALL)
for concert in scrape_ALL:
    print(concert)
    # for info in concert:
    #     print(info)
    print("="*100)