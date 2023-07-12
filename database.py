import mysql.connector
from logins import database_login

host, user, password, database = database_login()

connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = connection.cursor()

band_name = "Vader"

def instert_band_name(band_name):
    cursor.execute("INSERT INTO bands (band_name) VALUES (%s)", (band_name,))
    print(f"Inserted {band_name} into 'bands'")

def add_band_genre(band_name):
    # TODO dodać API metalarchives
    band_genre = "Death metal"

    cursor.execute("UPDATE bands SET band_genre = %s WHERE band_name = %s", (band_genre,band_name))

connection.commit()
cursor.close()
connection.close()
