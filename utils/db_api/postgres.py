import psycopg2
from psycopg2._psycopg import DatabaseError

import logging


class Database:
    def __init__(self):
        # connecting to existing database
        self.connection = psycopg2.connect(user="postgres",
                                           password="toor",
                                           host="127.0.0.1",
                                           port="5432",
                                           database="postgres")
        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor = self.connection.cursor()

        # peerspace table creation
        sql = """
                        CREATE TABLE IF NOT EXISTS peerspace (
                        listing_url VARCHAR(255) NOT NULL,
                        location_name VARCHAR(255),
                        host_name VARCHAR(255),
                        address VARCHAR(255),
                        phone_number VARCHAR(255),
                        review_count INT,
                        date_created TIMESTAMP,
                        PRIMARY KEY (listing_url)
                        )
                        """

        self.cursor.execute(sql)
        self.connection.commit()

        logging.info('[ DATABASE ]: Table for peerspace.com was created successfully')

        # splacer table creation
        sql = """
                        CREATE TABLE IF NOT EXISTS splacer (
                        listing_url VARCHAR(255) NOT NULL,
                        location_name VARCHAR(255),
                        host_name VARCHAR(255),
                        address VARCHAR(255),
                        phone_number VARCHAR(255),
                        review_count INT,
                        date_created TIMESTAMP,
                        PRIMARY KEY (listing_url)
                        )
                        """
        self.cursor.execute(sql)
        self.connection.commit()
        logging.info('[ DATABASE ]: Table for slpacer.com was created successfully')
        self.cursor.close()

    def add_listing(self, table_name, listing_url, location_name, host_name, address, phone_number, review_count, date_created):
        try:
            sql = "INSERT INTO " + str(
                table_name) + " (listing_url, location_name, host_name, address, phone_number, review_count, date_created) VALUES (%s,%s,%s,%s,%s,%s,%s)"

            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, (
            listing_url, location_name, host_name, address, phone_number, review_count, date_created))
            self.connection.commit()
            self.cursor.close()
        except DatabaseError:
            self.cursor = self.connection.cursor()
            self.cursor.execute("ROLLBACK")
            self.connection.commit()
            self.cursor.close()
