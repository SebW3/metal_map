import time
import requests
from bs4 import BeautifulSoup
import re
import openAI
import datetime
# from selenium import webdriver
# import facebook
# from logins import facebook_api_login
# from database import chceck_source

class WebScraper:
    concerts = []
    def __init__(self, url):
        self.url = url

    def openAI(self, description=None):
        # analise description for concert info
        temp = openAI.bands_from_description(description)
        print(temp)
        return temp
        # TODO

    def scrape_data(self, specific_event_link=None, num_events=None, ALL=None):
        if "facebook" in self.url:
            return self.scrape_facebook_data()
        elif "rockmetal" in self.url:
            return self.scrape_rockmetal_data(specific_event_link, num_events, ALL)
        elif "biletomat" in self.url:
            return self.scrape_biletomat_data(specific_event_link, num_events, ALL)
        else:
            print("unknown website")
            return None

    def scrape_rockmetal_data(self, specific_event_link=None, num_events=None, ALL=None):
        # functions
        def f_specific_event_link(specific_event_link):
            print("downloading specific event data")
            response = requests.get(specific_event_link)

            concert_number = int((specific_event_link).split("koncert=")[1][:5])
            soup = BeautifulSoup(response.content, "html.parser")
            concert_element = soup.find_all(class_="gigItemIn")
            concerts = []
            for element in concert_element:  # multiple plays in one event
                concert_element_text = element.get_text().splitlines()

                data = []
                title = soup.find_all(class_="gigItemTitle")
                if title:
                    title = str(title[0])[25:-5]
                else:
                    title = None
                bands_playing = []
                localization = [None, None, None]  # place, club, address
                price = None
                added_date = None
                change_date = None
                concert_date = None
                additional_info = None

                for element in concert_element_text:
                    if element == "" or len(element) <= 2 and not "zł" in element:  # skip non-printable
                        continue
                    data.append(element.strip())

                for i in range(len(data)):
                    if data[i] == "Wystąpi:":
                        if ":" not in data[i+1]:
                            bands_playing.append(data[i+1])
                    elif data[i] == "Wystąpią:" or data[i] == "Wystąpili:":
                        j = 1
                        while ":" not in data[i+j]:
                            bands_playing.append(data[i+j])
                            j += 1
                    elif data[i] == "Kiedy:":
                        concert_date = data[i+1].split()[0]
                    elif data[i] == "Gdzie:":
                        for j in range(len(localization)-1):
                            if ":" in data[i+j+1]:
                                break
                            localization[j] = data[i+j+1]
                    elif data[i] == "Cena:":
                        price = data[i+1]
                    elif "Dodane:" in data[i]:
                        if "zmiana" in data[i]:
                            added_date = data[i].split(",")[0][8:]
                            change_date = data[i].split(",")[1].strip()[8:]
                        else:
                            added_date = data[i][8:]
                    elif data[i] == "Uwagi:":
                        additional_info = data[i+1]


                if "(www)" in bands_playing:
                    bands_playing.remove("(www)")


                print([concert_number, title, bands_playing, concert_date, localization, price, added_date, change_date, additional_info, None, "rockmetal.pl"])

                if len(concert_element) == 1:  # if NOT festival return info, otherwise continue appending data
                    return [concert_number, title, bands_playing, concert_date, localization, price, added_date, change_date, additional_info, None, "rockmetal.pl"]
                concerts.append([concert_number, title, bands_playing, concert_date, localization, price, added_date, change_date, additional_info, None, "rockmetal.pl"])

            return [concerts]

        def f_num_events(num_events):
            return f_ALL(num_events)

        def f_ALL(num_events=None):
            if num_events:
                print(f"downloading {num_events} events")
            else:
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

                if num_events:
                    if len(links) <= num_events:
                        break
                break  # working on smaller dataset for now

            data_ALL = []
            i = 0
            for link in links:
                print(link)
                data_ALL.append([f_specific_event_link(link)])

                i += 1  # temp
                if i > 3:
                    break

                if num_events:
                    if i >= num_events:
                        print(f"downloaded {num_events} events")
                        break


                print("timer 1 sec")
                time.sleep(1)

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

    def scrape_biletomat_data(self, specific_event_link=None, num_events=None, ALL=None):  # this one will use openAI to analyse text
        def f_specific_event_link(specific_event_link):
            print("downloading specific event data")

            response = requests.get(specific_event_link)
            soup = BeautifulSoup(response.content, "html.parser")
            header = soup.find(class_="product-header__details")

            concert_info = header.get_text().replace("\n\n\n", "").replace("  ", "")

            concert_info = concert_info.splitlines()

            for item in concert_info:  # remove whitespaces
                if len(item) < 2:
                    concert_info.remove(item)

            concert_number = specific_event_link.split("-")[-1][:-1]
            title = soup.find(class_="product-header__title").get_text().strip()
            concert_date = concert_info[0].split()[0] + " " + concert_info[0].split()[-1]
            localization = [concert_info[5], concert_info[2] + concert_info[3]]
            change_date = datetime.date.today().strftime('%d.%m.%Y')  # no info on the website
            description = soup.find_all(class_="description-block__text-block")[1].get_text().strip()
            bands_playing = [openAI.bands_from_description(description)]

            if bands_playing[0] == "n/a":
                # if band name not found in description then it is most likely in the title
                bands_playing = [title.split()[0].lower().capitalize()]

            # TODO ticket_price, short_description
            ticket_price = soup.find(class_="tickets-list__list").find(class_="ticket-card__pricing").get_text().split()[0].strip() + " zł"
            short_description = openAI.create_short_description(description)

            print([concert_number, title, bands_playing, concert_date, localization, ticket_price, None, change_date, None, short_description, "biletomat.pl"])
            # [concert_number, title, bands_playing, concert_date, localization, ticket_price, added_date, change_date, additional_info, short_description, source]
            return [concert_number, title, bands_playing, concert_date, localization, ticket_price, None, change_date, None, short_description, "biletomat.pl"]


        def f_ALL(num_events=None):
            response = requests.get("https://www.biletomat.pl/metal/")
            soup = BeautifulSoup(response.content, "html.parser")
            links = soup.find_all(class_="event-teaser__link")

            for i in range(len(links)):
                temp = re.findall(r'"([^"]*)"', str(links[i]))
                links[i] = temp[1]
            print(len(links), links)

            i = 1
            concerts_desc = []
            for link in links:
                concert = f_specific_event_link(link)
                concerts_desc.append([concert])

                print("timer 1 sec")
                time.sleep(1)

                if i >= 2:
                    break
                i += 1

            return concerts_desc

        if specific_event_link:
            return f_specific_event_link(specific_event_link)
        # TODO
        # elif num_events:
        #    return f_num_events(num_events)
        elif ALL:
            return f_ALL()
        else:
            print("please specify what to scrape")
            pass
