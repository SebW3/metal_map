# temporary code here
from WebScraper import WebScraper
from database import Database

# Testing here
rockmetal_scraper = WebScraper("rockmetal")

concerts = rockmetal_scraper.scrape_data(num_events=2)
# #concerts = rockmetal_scraper.scrape_data(specific_event_link="https://www.rockmetal.pl/koncerty.html?koncert=56215_Pol_and_Rock_Festival")
# #concerts = rockmetal_scraper.scrape_data(specific_event_link="https://www.rockmetal.pl/koncerty.html?koncert=57152_Summer_Dying_Loud_XIV")
# print("&%"*100)
# print("all downloaded concerts", concerts)
#
database = Database()

#database.add_concert_to_database(concerts)

for concert in concerts:
     print(concert)
     database.add_concert_to_database(concert)




url = "https://www.biletomat.pl/bilety/sacramental-petrification-of-europe-2023-13491/"
scrape_data = WebScraper("biletomat")



concerts = scrape_data.scrape_data(ALL=True)
print("hello", concerts)

database.add_concert_to_database(concerts)

# for concert in concerts:
#     print(concert)
#     database.add_concert_to_database(concert)

database.close_db_connection()
