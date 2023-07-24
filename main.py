# temporary code here
# import WebScraper
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

url = "https://winiarybookings.pl/wydarzenia"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
print(soup)

print("==="*100)



driver = webdriver.Firefox()
driver.get(url)

page_content = driver.page_source
time.sleep(3)
driver.quit()

soup = BeautifulSoup(page_content, 'html.parser')
soup = soup.decode()
#soup = soup.replace("\n", "")
print(soup)