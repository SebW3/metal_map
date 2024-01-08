import time
import requests
from bs4 import BeautifulSoup
import re
import openAI
import datetime
from selenium import webdriver
from logins import profile_path
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

    def scrape_data(self, specific_event_link=None, num_events=None, ALL=None, site=None, page=None):
        if "facebook" in self.url:
            return self.scrape_facebook_data(site, page, ALL)
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
                            change_date = added_date
                    elif data[i] == "Uwagi:":
                        additional_info = data[i+1]


                if "(www)" in bands_playing:
                    bands_playing.remove("(www)")


                print([concert_number, title, bands_playing, concert_date, localization, price, added_date, change_date, additional_info, None, "rockmetal.pl"])

                if len(concert_element) == 1:  # if NOT festival return info, otherwise continue appending data
                    return [concert_number, title, bands_playing, concert_date, localization, price, added_date, change_date, additional_info, None, specific_event_link]
                concerts.append([concert_number, title, bands_playing, concert_date, localization, price, added_date, change_date, additional_info, None, specific_event_link])

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

    def scrape_facebook_data(self, site=None, page=None, ALL=None):
        def get_newest_event_id(url):
            driver = webdriver.Firefox()
            driver.get(url)

            page_content = driver.page_source
            driver.quit()

            soup = BeautifulSoup(page_content, 'html.parser')

            # test
            links = soup.find_all(href="")

            test_links = []
            i = 0
            for link in links:
                link_text = link.get_text()
                if "https:\/\/www.facebook.com\/events\/" in link_text:
                    test_links.append(link)

            try:
                text = test_links[0].decode()
            except:
                print("No upcoming events on this page")
                return None

            event_id = text.split("https:\/\/www.facebook.com\/events\/")[1][:16]
            print("facebook event id = ", event_id)

            return event_id


        def read_event_info(event_id):
            if event_id is None:
                return None
            driver = webdriver.Firefox(firefox_profile=profile_path())
            driver.get(f"https://www.facebook.com/events/{event_id}/")
            time.sleep(3)
            page_source = driver.page_source

            soup = BeautifulSoup(page_source, "html.parser")

            elements = soup.find_all(role="button")
            for element in elements:
                if "See more" in element.get_text():
                    button = driver.find_element_by_xpath('//div[@role="button" and text()="See more"]')
                    button.click()
                    page_source = driver.page_source
                    driver.quit()
                    soup = BeautifulSoup(page_source, "html.parser")
                    details = soup.find(class_="x1l90r2v xyamay9")
                    description = details.find(class_="x1pi30zi x1swvt13")
                    print(description.get_text())
                    details.find(class_="x1pi30zi x1swvt13").extract()


                    localization = soup.find(class_="x9f619 x1n2onr6 x1ja2u2z xeuugli x1iyjqo2 xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj xnp8db0 x65f84u x1xzczws").find_all(class_="xu06os2 x1ok221b")
                    club = localization[0].get_text()
                    address = localization[1].get_text().split(",")[0].replace("ulica", "").strip()
                    print("===")
                    concert_info = openAI.get_info_from_fb_desc(description.get_text()).split(";")
                    print(concert_info)

                    concert_number = event_id
                    title = soup.find(class_="x78zum5 xdt5ytf x1wsgfga x9otpla").find(class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6").get_text().strip()
                    bands_playing = []
                    if "n/a" not in concert_info[0]:
                        bands_playing_from_fb = concert_info[0].replace("Zespoły: ", "")
                        temp = bands_playing_from_fb.split(", ")
                        for band_and_genre in temp:
                            band = band_and_genre.split("(")[0].strip()
                            #genre = band_and_genre.split("(")[1].replace(")", "").replace("/", ", ").strip() # TODO add to band genre database
                            bands_playing.append(band)

                    concert_date = None
                    if "n/a" not in concert_info[1]:
                        concert_date = concert_info[1].replace("Data i godzina: ", "").strip()
                    # city = concert_info[2].split()[-1].strip() # TODO AI prompt
                    city = concert_info[-1].replace("Miasto koncertu: ", "").replace(".", "").strip()
                    localization = [city, club, address]
                    price = None
                    if "n/a" not in concert_info[3]:
                        price = concert_info[3].replace("Cena biletu: ", "").split()[0].strip()
                    added_date = None # TODO post date
                    change_date = datetime.date.today().strftime('%d.%m.%Y')  # no info on the website
                    additional_info = None

                    return [concert_number, title, bands_playing, concert_date, localization, price, added_date, change_date, additional_info, None, f"https://www.facebook.com/events/{event_id}/"]


        if ALL == True:
            # use all functions
            pass
        elif page != None:
            event_id = get_newest_event_id(f"https://www.facebook.com/{page}")
            return read_event_info(event_id)
        else:
            print("please specify page")
        pass

    def scrape_biletomat_data(self, specific_event_link=None, num_events=None, ALL=None):  # this one will use openAI to analyse text
        def f_specific_event_link(specific_event_link):
            print("downloading specific event data")

            response = requests.get(specific_event_link)
            soup = BeautifulSoup(response.content, "html.parser")

            concert_number = specific_event_link.split("-")[-1][:-1]
            title = soup.find(class_="product-header__title").get_text().strip()
            temp = ""
            if len(soup.find(class_="product-detail__description").get_text()) > 2:
                godz = soup.find(class_="product-detail__description").get_text().strip()
                temp = ", " + godz[-5:]
            concert_date = soup.find(class_="product-detail").get_text().split(", ")[0].strip() + temp.strip()
            localization = [soup.find(itemprop="addressLocality").get_text(), soup.find(itemprop="location").find(itemprop="name").get_text().split(",")[0] + ", " + soup.find(itemprop="streetAddress").get_text()]
            change_date = datetime.date.today().strftime('%d.%m.%Y')  # no info on the website
            description = soup.find_all(class_="description-block__text-block")[1].get_text().strip()
            bands_playing = [openAI.bands_from_description(description)]

            if bands_playing[0] == "n/a":
                # if band name not found in description then it is most likely in the title
                bands_playing = [title.split()[0].lower().capitalize()]


            ticket_price = soup.find(class_="tickets-list__list").find(class_="ticket-card__pricing").get_text().split()[0].strip() + " zł"
            #short_description = openAI.create_short_description(description)
            short_description = None

            print([concert_number, title, bands_playing, concert_date, localization, ticket_price, None, change_date, None, short_description, "biletomat.pl"])
            # [concert_number, title, bands_playing, concert_date, localization, ticket_price, added_date, change_date, additional_info, short_description, source]
            return [concert_number, title, bands_playing, concert_date, localization, ticket_price, None, change_date, None, short_description, specific_event_link]


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
