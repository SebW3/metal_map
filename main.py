# temporary code here
from WebScraper import WebScraper
import database


# Testing here
rockmetal_scraper = WebScraper("rockmetal")
specific_event_data = rockmetal_scraper.scrape_data("https://www.rockmetal.pl/koncerty.html?koncert=56347_Wardruna_Percival")
print("concert data: ", specific_event_data)
#database.add_concert_to_database(specific_event_data)
scrape_ALL = rockmetal_scraper.scrape_data(ALL=True)
print("|"*200)
print(scrape_ALL)
for concert in scrape_ALL:
     database.add_concert_to_database(concert)
#     # for info in concert:
#     #     print(info)
#     print("="*100)

