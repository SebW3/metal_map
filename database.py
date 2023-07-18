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
