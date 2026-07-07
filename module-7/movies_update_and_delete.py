# Roxanne Buenaventura
# CSD-310
# Assignment 6_2
# 5 July 2026

""" import statements """
import mysql.connector
from mysql.connector import errorcode

import dotenv
from dotenv import dotenv_values

# using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

try:
    """ try/catch block for handling potential MySQL database errors """

    # connect to the database
    db = mysql.connector.connect(**config) #connect to the movies databse

    #create cursor
    cursor = db.cursor()
    
    # output the connection status
    print(
        "\nDatabase user {} connected to MySQL on host {} with database {}".format(
            config["user"],
            config["host"],
            config["database"]
        )
    )
    def show_films(cursor, title):
        print(f"\n-- {title} --")

        cursor.execute("""
            SELECT
                film_name AS Name,
                film_director AS Director,
                genre_name AS Genre,
                studio_name AS Studio
            FROM film
            INNER JOIN genre
                ON film.genre_id = genre.genre_id
            INNER JOIN studio
                ON film.studio_id = studio.studio_id;
        """)

        films = cursor.fetchall()

        for film in films:
            print(f"Film Name: {film[0]}")
            print(f"Director: {film[1]}")
            print(f"Genre Name ID: {film[2]}")
            print(f"Studio Name: {film[3]}")
            print()

    show_films(cursor, "DISPLAYING FILMS")

    cursor.execute("""
        INSERT INTO film (
            film_name,
            film_releaseDate,
            film_runtime,
            film_director,
            studio_id,
            genre_id
        )
        VALUES (
            "Insidious",
            2010,
            102,
            "James Wan",
            2,
            1
        )
    """)
    cursor.execute("""
        UPDATE film
        SET genre_id = 1
        WHERE film_name = "Alien"
    """)

    cursor.execute("""
        DELETE FROM film
        WHERE film_name = 'Gladiator'
    """)

    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")


        
    input("\n\nPress Enter to continue...")

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """

    if "cursor" in locals(): # close cursor
        cursor.close()

    if "db" in locals() and db.is_connected():
        db.close()