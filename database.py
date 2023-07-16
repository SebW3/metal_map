import mysql.connector
from logins import database_login
import metalarchives

host, user, password, database = database_login()

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor= connection.cursor()
print("Connected do database")

# TODO gathering band names
band_name = "Metallica"

def instert_band_name_and_genre(band_name):
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

def add_band_genre(band_name):
    band_genre = metalarchives.get_genre(band_name)

    if band_genre:
        cursor.execute("UPDATE bands SET band_genre = %s WHERE band_name = %s", (band_genre,band_name))
        print(f"band genre {band_genre} added to band named {band_name}")
        connection.commit()
    return None

# # chceck if band genre already exists
# cursor.execute("SELECT band_genre FROM bands WHERE band_name = %s", (band_name,))
# temp = cursor.fetchone()[0]
# if temp == None:
#     print("add genre")
#     #add_band_genre(band_name)

def add_band_info_to_database(band_name):
    # chceck if band genre already exists
    cursor.execute("SELECT band_name FROM bands WHERE band_name = %s", (band_name,))
    temp = cursor.fetchone()
    print(temp)
    if temp == None:
        instert_band_name_and_genre(band_name)

def chceck_source(country, site, page, name):  # TODO think of something better
    connection = mysql.connector.connect(  # TODO find a way to avoid copying this
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()
    print("Connected do database")


    if name == "Thrash Attack Lublin":
        cursor.execute("SELECT number FROM concerts_info_source WHERE name = %s", (name,))
        cursor.close()
        connection.close()
        return cursor.fetchone()

cursor.close()
connection.close()
