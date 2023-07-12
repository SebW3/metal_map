from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

driver = webdriver.Firefox()
band_name = "Necrophobic"
url = f"https://www.metal-archives.com/search/advanced/searching/bands?bandName={band_name}&exactBandMatch=1&genre=&country=&yearCreationFrom=&yearCreationTo=&bandNotes=&status=1&themes=&location=&bandLabelName=#bands"

driver.get(url)
while True:  # waiting for scripts to load
    page_content = driver.page_source
    if 'tr class="odd"' in page_content:
        break
    time.sleep(1)
    print("waiting 1 sec "*100)

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
    print("Znaleziono zawartość:", result)
    temp = result.split("class")
    print(temp)
    band_genre = temp[2][4:-9]
    print(band_genre)
else:
    print("Nie znaleziono znacznika 'jest'")
