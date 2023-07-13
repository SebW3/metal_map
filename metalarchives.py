# This code changes link to search for active band with exact name (only active bands play)
# Then it waits for scripts to load and extracts band genre for later use
# TODO rebuild this "API" to not use user browser
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

def get_genre(band_name):
    driver = webdriver.Firefox()

    url = f"https://www.metal-archives.com/search/advanced/searching/bands?bandName={band_name}&exactBandMatch=1&genre=&country=&yearCreationFrom=&yearCreationTo=&bandNotes=&status=1&themes=&location=&bandLabelName=#bands"

    driver.get(url)
    while True:  # waiting for scripts to load
        page_content = driver.page_source
        if 'tr class="odd"' in page_content:
            break
        time.sleep(1)
        print("waiting 1 sec...")

    driver.quit()

    soup = BeautifulSoup(page_content, 'html.parser')
    soup = soup.decode()

    def find_content(text):
        pattern = r'<tr class="odd"(.*)'
        match = re.search(pattern, text)
        if match:
            content = match.group(1)
            return content.strip()
        else:
            return None

    result = find_content(soup)
    if result:
        temp = result.split("class")
        band_genre = temp[2][4:-9]
        return band_genre
    else:
        return None
