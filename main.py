# temporary code here
from WebScraper import WebScraper
from database import Database

# Testing here
database = Database()

#database.add_concert_to_database(concerts)

# for concert in concerts:
#      print(concert)
#      database.add_concert_to_database(concert)



#
# url = "https://www.biletomat.pl/bilety/sacramental-petrification-of-europe-2023-13491/"
# scrape_data = WebScraper("biletomat")
#
#
#
# concerts = scrape_data.scrape_data(ALL=True)
#
#
#
# for concert in concerts:
#     print(concert)
#     database.add_concert_to_database(concert)
#
# database.close_db_connection()

# rocmetal = WebScraper("rockmetal")
# biletomat = WebScraper("biletomat")
#
# concert = rocmetal.scrape_data(specific_event_link="https://www.rockmetal.pl/koncerty.html?koncert=57068_In_the_Woods____Saturnus_The_Foreshadowing")
# database.add_concert_to_database([concert])
#
# concert = (biletomat.scrape_data(specific_event_link="https://www.biletomat.pl/bilety/in-the-woods-saturnus-krakow-14154/"))
# database.add_concert_to_database([concert])

rockmetal = WebScraper("rockmetal")
concerts = rockmetal.scrape_data(num_events=1)
for concert in concerts:
    database.add_concert_to_database(concert)

print(database.normalize_band_names([1, 6], from_id_to_name=True))

database.close_db_connection()