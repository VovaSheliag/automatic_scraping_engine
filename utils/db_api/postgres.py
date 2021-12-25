import psycopg2
from psycopg2 import Error


class Database:
    def __init__(self):
        # connecting to existing database
        self.connection = psycopg2.connect(user="postgres",
                                           password="toor",
                                           host="127.0.0.1",
                                           port="5432",
                                           database="postgres")

        self.cursor = self.connection.cursor()
        # table creation
        create_table_query = '''CREATE TABLE IF NOT EXISTS test_table
                                  (ID INT PRIMARY KEY     NOT NULL,
                                  MODEL           TEXT    NOT NULL,
                                  PRICE         REAL); '''

        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("Test table was successfully created")
        self.cursor.close()
