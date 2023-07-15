# TODO scraping the same way like in metalarchives.py
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

def from_Thrash_Attack_Lublin():
    url = "https://www.facebook.com/ThrashAttackLublin"
    driver = webdriver.Firefox()
    driver.get(url)

    page_content = driver.page_source
    time.sleep(3)
    driver.quit()

    soup = BeautifulSoup(page_content, 'html.parser')
    soup = soup.decode()
    soup = soup.replace("\n", "")

    zmienna = "Thrash Attack Lublin #58"
    pattern = rf'{zmienna}(.*?)"'

    match = re.search(pattern, soup)

    if match == None:
        print("no link found")
        return None

    result = match.group(1)
    ID = result.split("/")
    ID = ID[-2]

    return ID[:-1]

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def event_Thrash_Attack_Lublin(event_link):
    driver = webdriver.Firefox()
    driver.get(event_link)

    time.sleep(3)

    # Pobierz zawartość strony
    page_content = driver.page_source
    #print(page_content)

    # # Poczekaj maksymalnie 10 sekund, aż przycisk pojawi się na stronie
    # wait = WebDriverWait(driver, 1)
    # decline_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Decline optional cookies')]")))

    # Znajdź przycisk na stronie
    try:
        decline_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Decline optional cookies')]")
        print("próbowałem")
        # Kliknij przycisk, jeśli jest widoczny i aktywny
        if decline_button.is_displayed() and decline_button.is_enabled():
            decline_button.click()
            print("znaleziono")
    except:
        pass
        print("chuj nie działa")

    # Kliknij przycisk
    #decline_button.click()

    # Poczekaj kolejne 3 sekundy, aby upewnić się, że strona zdążyła się załadować po kliknięciu
    time.sleep(3)

    # Pobierz zawartość strony
    page_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_content, 'html.parser')
    soup = soup.decode()
    print(soup)

event_link = from_Thrash_Attack_Lublin()
print(event_link)
# event_Thrash_Attack_Lublin(event_link)
#url = "https://facebook.com/events/s/thrash-attack-lublin-58/1446993666051348/"
url = event_link


### facebook bad
import facebook
from logins import facebook_api_login

access_token = facebook_api_login()
api = facebook.GraphAPI(access_token)

# Wprowadź tutaj ID lub URL wydarzenia, które chcesz pobrać
event_id = '1446993666051348'

try:
    # Pobierz dane wydarzenia
    event_data = api.get_object(event_id, fields='id,name,description,start_time,end_time')

    # Przetwórz dane wydarzenia i przygotuj tekst do zapisu
    event_info = f"Event ID: {event_data['id']}\n"
    event_info += f"Event Name: {event_data['name']}\n"
    event_info += f"Start Time: {event_data['start_time']}\n"

    # Sprawdź, czy klucz 'end_time' istnieje w danych wydarzenia
    if 'end_time' in event_data:
        event_info += f"End Time: {event_data['end_time']}\n"

    if 'description' in event_data:
        event_info += f"Description: {event_data['description']}\n"

    print(event_info)

except facebook.GraphAPIError as e:
    print(f"Wystąpił błąd: {e}")