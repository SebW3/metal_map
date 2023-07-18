import time
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import facebook
from logins import facebook_api_login
from database import chceck_source


def from_Thrash_Attack_Lublin():  # TODO rebuild this but good enough for now
    url = "https://www.facebook.com/ThrashAttackLublin"
    driver = webdriver.Firefox()
    driver.get(url)

    page_content = driver.page_source
    #time.sleep(3)
    driver.quit()

    soup = BeautifulSoup(page_content, 'html.parser')
    soup = soup.decode()
    soup = soup.replace("\n", "")

    concert = "Thrash Attack Lublin #" + str(chceck_source("Poland", "Facebook", None, "Thrash Attack Lublin")[0])
    print(concert)
    pattern = rf'{concert}(.*?)"'

    match = re.search(pattern, soup)

    if match == None:
        print("no link found")
        return None

    result = match.group(1)
    ID = result.split("/")
    ID = ID[-2]

    return ID[:-1]

def event_Thrash_Attack_Lublin(event_ID):
    access_token = facebook_api_login()
    api = facebook.GraphAPI(access_token)

    try:
        event_data = api.get_object(event_ID, fields='id,name,description,start_time,end_time')


        event_info = f"Event ID: {event_data['id']}\n"
        event_info += f"Event Name: {event_data['name']}\n"
        event_info += f"Start Time: {event_data['start_time']}\n"
        desc = f"Description: {event_data['description']}"

        print(event_info)

        print(desc)
        parts = desc.split("\n\n")
        for i in range(1, len(parts)-1):
            print("="*100)
            # print(parts[i])
            # TODO RegEx band name and genre

        # extracting data about ticket cost
        data = parts[len(parts)-1].split("\n")
        ticket_price = data[3][7:]
        print(ticket_price)
        # TODO add to database


    except facebook.GraphAPIError as e:
        print(f"Wystąpił błąd: {e}")

i = 1
while True:
    #event_ID = from_Thrash_Attack_Lublin()
    event_ID = "1446993666051348"  # temp
    print("Event ID = ", event_ID)
    try:
        int(event_ID)  # check if valid ID
        #event_ID = "1446993666051348"  # temp
        event_Thrash_Attack_Lublin(event_ID)
        break
    except:
        print("Not valid event ID")
        i += 1
        print(f"Trying for {i} time")
        if i == 3:
            break