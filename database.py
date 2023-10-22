import mysql.connector
from logins import database_login
import metalarchives
from datetime import datetime

# TODO gathering band names

class Database:
    def __init__(self):
        self.cursor = None
        self.connection = None
        self.connect_to_db()

    def connect_to_db(self):
        host, user, password, database = database_login()
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        print("Connected do database")

    def close_db_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection to database closed")

    def check_if_already_exist(self, concert_number=None, concert_name=None, change_date=None, concert=None):
        # returns None if no entry
        # returns 1 if already exists with latest update
        # returns 2 if already exists without latest update


        def chceck_if_duplicate(concert=None):
            print("chcecking if duplicate exists", concert)
            concert_name = concert[1]
            bands_playing = ""
            for band in concert[2]:
                bands_playing += band + ", "
            bands_playing = bands_playing[:-2]
            concert_date = concert[3]
            concert_localization = concert[4]
            ticket_price = concert[5]
            change_date = concert[7]
            print("change date ", change_date)
            short_description = concert[9]
            source = concert[10]
            self.cursor.execute(f"SELECT id, name, bands_playing, concert_date, localization, ticket_price, change_date, short_description, source FROM concerts_poland WHERE concert_date LIKE '%{concert_date[:5]}%' AND localization LIKE '%{concert_localization[0]}%'")
            concert_in_db = self.cursor.fetchall()[0]
            print(concert_in_db)
            if short_description == None: # TODO something is not working
                short_description = concert_in_db[7] # bug?
                if short_description == "None":
                    short_description = None


            for band in bands_playing:
                if band in concert_in_db[2]:
                    # updating concert info
                    if concert_name and concert_in_db[1] == None:
                        self.cursor.execute(f"UPDATE concerts_poland SET name = '{concert_name}' WHERE id = {concert_in_db[0]}")
                        self.connection.commit()
                        print("updated name")

                    print(concert_in_db[6], change_date)
                    if concert_in_db[5]:  # change_date # check if new info (most recent update)
                        if change_date:
                            if datetime.strptime(change_date, "%d.%m.%Y").strftime("%Y.%m.%d") <= datetime.strptime(concert_in_db[6], "%d.%m.%Y").strftime("%Y.%m.%d"):
                                return None
                        else:
                            return None
                    else:
                        return None
                    # update info in database
                    if "rockmetal" in concert_in_db[8]:  # the most accurate info
                        concert_localization = concert_in_db[4]

                    source = concert_in_db[8] + " " + source

                    self.cursor.execute(f"UPDATE concerts_poland SET bands_playing = '{bands_playing}', localization = '{concert_localization}', ticket_price = '{ticket_price}', change_date = '{change_date}', short_description = '{short_description}', source = '{source}' WHERE id = {concert_in_db[0]}")
                    self.connection.commit()
                    print("changes committed")
                    return True

            print("it is not a duplicate")
            return False

        try:
            if chceck_if_duplicate(concert=concert) != False: return 1
        except:
            pass

        # check by concert_name
        if concert_name:  # TODO potential bug if same concert repeats # temp fix 3 lines below
            self.cursor.execute("SELECT name FROM concerts_poland WHERE name = %s", (concert_name,))

            try:
                concert_name_db = self.cursor.fetchone()
            except:
                concert_name_db = self.cursor.fetchall[0]
            if concert_name_db:
                concert_name_db = concert_name_db[0]
            if concert_name == concert_name_db:
                self.cursor.execute(f"SELECT change_date FROM concerts_poland WHERE name = %s", (concert_name,))
                change_date_db = self.cursor.fetchone()

                if change_date_db:
                    change_date_db = change_date_db[0]

                if change_date_db == change_date or change_date_db == None:
                    print("newest info in database")
                    return 1
                else:
                    print("concert info update required")
                    return 2
            else:
                print(f"no {concert_name} in database")

                return None

        # check by concert_number
        self.cursor.execute(f"SELECT concert_number FROM concerts_poland WHERE concert_number = {concert_number}")
        concert_number_db = self.cursor.fetchone()
        if concert_number_db:
            concert_number_db = concert_number_db[0]
        # print(concert_number_db, "number in database")

        if concert_number == concert_number_db:
            self.cursor.execute(f"SELECT change_date FROM concerts_poland WHERE concert_number = {concert_number}")
            change_date_db = self.cursor.fetchone()
            if change_date_db:
                change_date_db = change_date_db[0]


            if change_date_db == change_date or change_date_db == None:
                print("newest info in database")
                return 1
            else:
                print("concert info update required")
                print(f"input date {change_date}, in database {change_date_db}")
                return 2
        else:
            print(f"no concert with concert_number {concert_number} in database")

            return None

    def add_concert_to_database(self, concerts):  # TODO add checking if already exists
        if len(concerts) > 1:  # festival
            print("adding festival info")


            check = self.check_if_already_exist(concert_name=concerts[0][1], concert_number=concerts[0][0])

            if check == 1:
                return 0
            elif check == 2:

                self.cursor.execute("SELECT festival_id FROM concerts_poland WHERE name = %s",
                               (concerts[0][1],))  # TODO error if same name
                festival_id = self.cursor.fetchone()[0]
                self.cursor.execute("DELETE FROM festivals WHERE festival_id = %s", (festival_id,))
                self.connection.commit()
                for concert in concerts:
                    print("_" * 100)
                    print(concert)

                    bands_playing = ""
                    for band in concert[2]:
                        bands_playing += band + ", "

                    localization = ""
                    try:
                        for localizatio in concert[4]:
                            localization += localizatio + ", "
                    except:
                        pass
                    print("adding concert info to database")

                    self.cursor.execute(
                        "INSERT INTO festivals (festival_id, title, bands_playing, concert_date, localization, ticket_price, added_date, change_date, additional_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (festival_id, concert[1], bands_playing[:-2], concert[3], localization[:-2], concert[5],
                         concert[6],
                         concert[7], concert[8]))
                self.connection.commit()


            else:
                self.cursor.execute("SELECT festival_id FROM festivals ORDER BY festival_id DESC LIMIT 1")
                latest_id = self.cursor.fetchone()[0] + 1
                for concert in concerts:
                    print("_" * 100)
                    print(concert)

                    bands_playing = ""
                    for band in concert[2]:
                        bands_playing += band + ", "

                    localization = ""
                    try:
                        for localizatio in concert[4]:
                            localization += localizatio + ", "
                    except:
                        pass
                    print("adding concert info to database")

                    self.cursor.execute(
                        "INSERT INTO festivals (festival_id, title, bands_playing, concert_date, localization, ticket_price, added_date, change_date, additional_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (latest_id, concert[1], bands_playing[:-2], concert[3], localization[:-2], concert[5],
                         concert[6],
                         concert[7], concert[8]))

                print("&" * 100)
                self.cursor.execute(
                    "INSERT INTO concerts_poland (concert_number, festival_id, name, concert_size, concert_date, localization, ticket_price, added_date, change_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (concert[0], latest_id, concert[1], "festival", concert[3], localization[:-2], concert[5],
                     concert[6], concert[7]))
                self.connection.commit()

        else:  # normal concert
            concert = concerts[0]
            check = self.check_if_already_exist(concert_number=concert[0], concert_name=concert[1], change_date=concert[7], concert=concert)
            if check == 1:  # newest info = no action needed
                return None
            else:  # adding / updating concert info
                bands_playing = ""
                for band in concert[2]:
                    bands_playing += band + ", "

                localization = ""
                try:
                    for localizatio in concert[4]:
                        localization += localizatio + ", "
                except:
                    pass
                print("adding concert info to database")


                if check == 2:
                    self.cursor.execute(
                        "UPDATE concerts_poland SET name = %s, concert_size = %s, bands_playing = %s, concert_date = %s, localization = %s, ticket_price = %s, added_date = %s, change_date = %s, additional_info = %s WHERE concert_number = %s",
                        (
                        concert[1], "medium", bands_playing[:-2], concert[3], localization[:-2], concert[5], concert[6],
                        concert[7], concert[8], concert[0]))
                    print("concert info updated")
                else:
                    self.cursor.execute(
                        "INSERT INTO concerts_poland (concert_number, name, concert_size, bands_playing, concert_date, localization, ticket_price, added_date, change_date, additional_info, short_description, source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (
                        concert[0], concert[1], "medium", bands_playing[:-2], concert[3], localization[:-2], concert[5],
                        concert[6], concert[7], concert[8], concert[9], concert[10]))
                    print("concert added")
                self.connection.commit()


    def add_band_info_to_database(self, band_name):
        def instert_band_name_and_genre(band_name):  # will I use it later?
            band_genre = metalarchives.get_genre(band_name)

            if band_genre:  # If this band exists
                self.cursor.execute("INSERT INTO bands (band_name) VALUES (%s)", (band_name,))
                print(f"Inserted {band_name} into 'bands'")
                self.connection.commit()

                self.cursor.execute("UPDATE bands SET band_genre = %s WHERE band_name = %s", (band_genre, band_name))
                print(f"band genre {band_genre} added to band named {band_name}")
                self.connection.commit()
            else:
                print("band is not on www.metal-archives.com")
                return None


        # chceck if band genre already exists
        self.cursor.execute("SELECT band_name FROM bands WHERE band_name = %s", (band_name,))
        temp = self.cursor.fetchone()
        print(temp)

        if temp == None:
            instert_band_name_and_genre(band_name)


    def chceck_source(self, country, site, page, name):  # TODO think of something better


        if name == "Thrash Attack Lublin":
            self.cursor.execute("SELECT number FROM concerts_info_source WHERE name = %s", (name,))
            temp = self.cursor.fetchone()

            return temp

# def add_band_genre(band_name):  # for manual adding
#     band_genre = metalarchives.get_genre(band_name)
#     if band_genre:
#         self.cursor.execute("UPDATE bands SET band_genre = %s WHERE band_name = %s", (band_genre,band_name))
#         print(f"band genre {band_genre} added to band named {band_name}")
#         self.connection.commit()
#
#     return None
