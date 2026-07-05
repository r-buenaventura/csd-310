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
# Query 1: Displaying studio records

    print("\n-- DISPLAYING Studio RECORDS --")

    cursor.execute("SELECT * FROM studio")

    for studio in cursor.fetchall():
        print("Studio ID:", studio[0])
        print("Studio Name:", studio[1])
        print()

    # Query 2: Displaying genre records

    print("\n-- DISPLAYING Genre RECORDS --")

    cursor.execute("SELECT * FROM genre")

    for genre in cursor.fetchall():
        print("Genre ID:", genre[0])
        print("Genre Name:", genre[1])
        print()

    # Query 3: Displaying Short film records

    print("\n-- DISPLAYING Short Film RECORDS --")

    cursor.execute("""
        SELECT film_name, film_runtime
        FROM film
        WHERE film_runtime < 120
    """)

    for film in cursor.fetchall():
        print("Film Name:", film[0])
        print("Runtime:", film [1])
        print()

    # Query 4: Displaying director records in order

    print("\n-- DISPLAYING Director RECORDS in Order --")

    cursor.execute("""
        SELECT film_name, film_director
        FROM film
        ORDER by film_director
    """)

    for film in cursor.fetchall():
        print("Film Name:", film[0])
        print("Director:", film [1])
        print()

    # Close cursor
    cursor.close()

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

    if "db" in locals() and db.is_connected():
        db.close()



