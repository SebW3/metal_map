# TODO clean code, merge some functions
# TODO rebuild code for less database connections
import mysql.connector
from logins import database_login
import metalarchives

# TODO gathering band names
band_name = "Xasthur"

def connect_to_db():
    host, user, password, database = database_login()
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()
    print("Connected do database")

    return connection, cursor

def close_db_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Connection to database closed")

# def add_band_genre(band_name):  # for manual adding
#     connection, cursor = connect_to_db()
#     band_genre = metalarchives.get_genre(band_name)
#
#     if band_genre:
#         cursor.execute("UPDATE bands SET band_genre = %s WHERE band_name = %s", (band_genre,band_name))
#         print(f"band genre {band_genre} added to band named {band_name}")
#         connection.commit()
#     close_db_connection(connection, cursor)
#     return None

def add_band_info_to_database(band_name):
    def instert_band_name_and_genre(band_name):  # will I use it later?
        band_genre = metalarchives.get_genre(band_name)

        if band_genre:  # If this band exists
            cursor.execute("INSERT INTO bands (band_name) VALUES (%s)", (band_name,))
            print(f"Inserted {band_name} into 'bands'")
            connection.commit()

            cursor.execute("UPDATE bands SET band_genre = %s WHERE band_name = %s", (band_genre, band_name))
            print(f"band genre {band_genre} added to band named {band_name}")
            connection.commit()
        else:
            print("band is not on www.metal-archives.com")
            return None

    connection, cursor = connect_to_db()
    # chceck if band genre already exists
    cursor.execute("SELECT band_name FROM bands WHERE band_name = %s", (band_name,))
    temp = cursor.fetchone()
    print(temp)

    if temp == None:
        instert_band_name_and_genre(band_name)
    close_db_connection(connection, cursor)

def chceck_source(country, site, page, name):  # TODO think of something better
    connection, cursor = connect_to_db()

    if name == "Thrash Attack Lublin":
        cursor.execute("SELECT number FROM concerts_info_source WHERE name = %s", (name,))
        temp = cursor.fetchone()
        close_db_connection(connection, cursor)
        return temp

def check_if_already_exist(concert_number=None, concert_name=None, change_date=None):
    # returns None if no entry
    # returns 1 if already exists with latest update
    # returns 2 if already exists without latest update
    connection, cursor = connect_to_db()

    # check by concert_name
    if concert_name:  # TODO potential bug if same concert repeats
        cursor.execute("SELECT name FROM concerts_poland WHERE name = %s", (concert_name,))

        concert_name_db = cursor.fetchone()
        if concert_name_db:
            concert_name_db = concert_name_db[0]
        if concert_name == concert_name_db:
            cursor.execute(f"SELECT change_date FROM concerts_poland WHERE name = %s", (concert_name,))
            change_date_db = cursor.fetchone()
            close_db_connection(connection, cursor)
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
            close_db_connection(connection, cursor)
            return None

    # check by concert_number
    cursor.execute(f"SELECT concert_number FROM concerts_poland WHERE concert_number = {concert_number}")
    concert_number_db = cursor.fetchone()
    if concert_number_db:
        concert_number_db = concert_number_db[0]
    #print(concert_number_db, "number in database")

    if concert_number == concert_number_db:
        cursor.execute(f"SELECT change_date FROM concerts_poland WHERE concert_number = {concert_number}")
        change_date_db = cursor.fetchone()
        if change_date_db:
            change_date_db = change_date_db[0]

        close_db_connection(connection, cursor)
        if change_date_db == change_date or change_date_db == None:
            print("newest info in database")
            return 1
        else:
            print("concert info update required")
            print(f"input date {change_date}, in database {change_date_db}")
            return 2
    else:
        print(f"no concert with concert_number {concert_number} in database")
        close_db_connection(connection, cursor)
        return None

def add_concert_to_database(concerts):  # TODO add checking if already exists
    if len(concerts) > 1:  # festival
        print("adding festival info")
        connection, cursor = connect_to_db()

        check = check_if_already_exist(concert_name=concerts[0][1], concert_number=concerts[0][0])

        if check == 1:
            return 0
        elif check == 2:
            connection, cursor = connect_to_db()
            cursor.execute("SELECT festival_id FROM concerts_poland WHERE name = %s", (concerts[0][1],))  # TODO error if same name
            festival_id = cursor.fetchone()[0]
            cursor.execute("DELETE FROM festivals WHERE festival_id = %s", (festival_id,))
            connection.commit()
            for concert in concerts:
                print("_"*100)
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

                cursor.execute(
                    "INSERT INTO festivals (festival_id, title, bands_playing, concert_date, localization, ticket_price, added_date, change_date, additional_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (festival_id, concert[1], bands_playing[:-2], concert[3], localization[:-2], concert[5],
                     concert[6],
                     concert[7], concert[8]))
            connection.commit()
            close_db_connection(connection, cursor)

        else:
            cursor.execute("SELECT festival_id FROM festivals ORDER BY festival_id DESC LIMIT 1")
            latest_id = cursor.fetchone()[0] + 1
            for concert in concerts:
                print("_"*100)
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

                cursor.execute(
                    "INSERT INTO festivals (festival_id, title, bands_playing, concert_date, localization, ticket_price, added_date, change_date, additional_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (latest_id, concert[1], bands_playing[:-2], concert[3], localization[:-2], concert[5], concert[6],
                     concert[7], concert[8]))

            print("&"*100)
            cursor.execute("INSERT INTO concerts_poland (concert_number, festival_id, name, concert_size, concert_date, localization, ticket_price, added_date, change_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (concert[0], latest_id, concert[1], "festival", concert[3], localization[:-2], concert[5], concert[6], concert[7]))
            connection.commit()
            close_db_connection(connection, cursor)
    else:  # normal concert
        concert = concerts[0]
        check = check_if_already_exist(concert_number=concert[0], concert_name=concert[1], change_date=concert[7])
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

            connection, cursor = connect_to_db()
            if check == 2:
                cursor.execute(
                    "UPDATE concerts_poland SET name = %s, concert_size = %s, bands_playing = %s, concert_date = %s, localization = %s, ticket_price = %s, added_date = %s, change_date = %s, additional_info = %s WHERE concert_number = %s",
                    (concert[1], "medium", bands_playing[:-2], concert[3], localization[:-2], concert[5], concert[6],
                     concert[7], concert[8], concert[0]))
                print("concert info updated")
            else:
                cursor.execute(
                    "INSERT INTO concerts_poland (concert_number, name, concert_size, bands_playing, concert_date, localization, ticket_price, added_date, change_date, additional_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (concert[0], concert[1], "medium", bands_playing[:-2], concert[3], localization[:-2], concert[5], concert[6], concert[7], concert[8]))
                print("concert added")
            connection.commit()
            close_db_connection(connection, cursor)
