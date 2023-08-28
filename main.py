# temporary code here
from WebScraper import WebScraper
import database


# Testing here
rockmetal_scraper = WebScraper("rockmetal")

#concerts = rockmetal_scraper.scrape_data(num_events=2)
#concerts = rockmetal_scraper.scrape_data(specific_event_link="https://www.rockmetal.pl/koncerty.html?koncert=56215_Pol_and_Rock_Festival")
concerts = rockmetal_scraper.scrape_data(specific_event_link="https://www.rockmetal.pl/koncerty.html?koncert=57152_Summer_Dying_Loud_XIV")
print("&%"*100)
print("all downloaded concerts", concerts)

for concert in concerts:
     print(concert)
     database.add_concert_to_database(concert)
