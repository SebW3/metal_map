Metal concerts map
===
---
This project will scrape data about metal concerts and display them on a map. <br>
This is my first big project!

---
## Setup
### Required libraries:
- mysql.connector
- requests
- bs4
- openai
- selenium

### Browser setup
1. Install Firefox
2. Open firefox and create new profile (type "about:profiles" in search bar"
3. Copy path to profile Root Directory and paste it in #TODO file
4. Launch new profile and deny cookies on facebook

---
# How to use
You can scrape concert data from sites: <a href="https://www.rockmetal.pl/koncerty.html">rockmetal.pl</a>, <a href="https://www.biletomat.pl/metal/">biletomat.pl</a> and from public facebook groups

First <code>import WebScraper from WebScraper.py</code> and <code>from database import Database</code> into main file<br>
Then declare variable and choose website to scrape data from<br>
for example: <code>rocmetal = WebScraper("rockmetal")</code>
You can choose to scrape info from specific concert or to scrape all info

Data will be retuned in lists so to add them to database use this:<br>
<code>
for concert in concerts: database.add_concert_to_database(concert)
</code>
### Rockmetal.pl scraper
### Biletomat.pl scraper
### Facebook pages scraper
<i>API from facebook did not allow me to read upcoming event data and that's why I'm using selenium</i>

To scrape from facebook page type its name from web address<br>
<code>concert = facebook_data.scrape_data(page="ThrashAttackLublin")</code>
https://www.facebook.com/ThrashAttackLublin <br>
That way you will be able to gather data from different pages
