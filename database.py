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

def add_concert_to_database(concerts):  # TODO add checking if already exists
    if len(concerts) > 1:
        print("adding festival info")
        connection, cursor = connect_to_db()
        cursor.execute("SELECT festival_id FROM festivals ORDER BY festival_id DESC LIMIT 1")
        latest_id = cursor.fetchone()[0] + 1
        print(latest_id, type(latest_id))
        for concert in concerts:
            print("_"*100)
            print(concert)

            bands_playing = ""
            for band in concert[1]:
                bands_playing += band + ", "

            localization = ""
            try:
                for localizatio in concert[3]:
                    localization += localizatio + ", "
            except:
                pass
            print("adding concert info to database")


            cursor.execute(
                "INSERT INTO festivals (festival_id, title, bands_playing, concert_date, localization, ticket_price, added_date, change_date, additional_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (latest_id, concert[0], bands_playing[:-2], concert[2], localization[:-2], concert[4], concert[5],
                 concert[6], concert[7]))

        print("&"*100)
        cursor.execute("INSERT INTO concerts_poland (festival_id, name, concert_size, concert_date, localization, ticket_price, added_date, change_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (latest_id, concert[0], "festival", concert[2], localization[:-2], concert[4], concert[5], concert[6]))
        connection.commit()
        close_db_connection(connection, cursor)
    else:
        concert = concerts[0]
        bands_playing = ""
        for band in concert[1]:
            bands_playing += band + ", "

        localization = ""
        try:
            for localizatio in concert[3]:
                localization += localizatio + ", "
        except:
            pass
        print("adding concert info to database")

        connection, cursor = connect_to_db()
        cursor.execute(
            "INSERT INTO concerts_poland (name, concert_size, bands_playing, concert_date, localization, ticket_price, added_date, change_date, additional_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (concert[0], "medium", bands_playing[:-2], concert[2], localization[:-2], concert[4], concert[5], concert[6], concert[7]))

        connection.commit()
        close_db_connection(connection, cursor)
