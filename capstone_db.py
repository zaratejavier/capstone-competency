import sqlite3


def create_schema(cursor):
    with open('capstone_schema.sql') as sql_file:
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)

    connection.commit()


connection = sqlite3.connect('capstone_data.db')
cursor = connection.cursor()

create_schema(cursor)
