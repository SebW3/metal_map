# temporary code here
from WebScraper import WebScraper
import database


# Testing here
rockmetal_scraper = WebScraper("rockmetal")
# specific_event_data = rockmetal_scraper.scrape_data("https://www.rockmetal.pl/koncerty.html?koncert=56347_Wardruna_Percival")
# print("concert data: ", specific_event_data)
#database.add_concert_to_database(specific_event_data)
# scrape_ALL = rockmetal_scraper.scrape_data(ALL=True)
# print("|"*200)
# print(scrape_ALL)
# for concert in scrape_ALL:
#      print(concert)
#      #database.add_concert_to_database(concert)
#      for info in concert:
#           print(info)
#      print("="*100)

concerts = rockmetal_scraper.scrape_data(num_events=2)
print("&%"*100)
print("all downloaded concerts", concerts)

for concert in concerts:
     database.add_concert_to_database(concert)
     print(concert)
     # print(concert[0])
     # print(concert[0][0], concert[0][1], concert[0][len(concert[0])-2])
     #database.check_if_already_exist(concert_number=concert[0][0], concert_name=concert[0][1], change_date=concert[0][len(concert[0])-2])
#      try:  # TODO list in list
#           for info in concert:
#               print(info)
#      except:
#           pass
#      print("^"*50)