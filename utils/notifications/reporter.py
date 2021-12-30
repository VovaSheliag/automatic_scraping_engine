"""
Here is the Reporter class, that forms reports (.csv files) after parsing finished.
Works with postgres database to find new parsed listings
"""
import datetime
import csv


class Reporter:
    def __init__(self, db, parsing_started, parsing_finished):
        self.db = db
        self.PARSING_STARTED = parsing_started
        self.PARSING_FINISHED = parsing_finished

    def form_csv_report(self, table_name, new_listings):
        with open('reports/' + str(table_name) + '.csv', mode='w+', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(['Link', 'Location Name', 'Host Name', 'Address', 'Phone Number', 'Review Count'])

            for listing in new_listings:
                try:
                    writer.writerow(listing[:-1])
                except:
                    pass

    def parse_tables(self):
        tables_list = self.get_tables()

        for table in tables_list:
            new_listings = self.parse_table(table)
            self.form_csv_report(table, new_listings)

    def parse_table(self, table):
        sql = "SELECT * FROM " + str(table)
        self.db.cursor = self.db.connection.cursor()
        self.db.cursor.execute(sql)
        all_listings = self.db.cursor.fetchall()
        self.db.cursor.close()

        new_listings = []

        # check for new listings
        for listing in all_listings:
            if self.PARSING_STARTED - datetime.timedelta(days=4) < listing[-1] < self.PARSING_FINISHED:
                new_listings.append(listing)
        return new_listings

    def get_tables(self):
        """
        Returns a list of available databases to form report with
        """
        s = ""
        s += "SELECT"
        s += " table_schema"
        s += ", table_name"
        s += " FROM information_schema.tables"
        s += " WHERE"
        s += " ("
        s += " table_schema = 'public'"
        s += " )"
        s += " ORDER BY table_schema, table_name;"

        self.db.cursor = self.db.connection.cursor()
        self.db.cursor.execute(s)
        tables_list = [db_fetch[-1] for db_fetch in self.db.cursor.fetchall()]
        self.db.cursor.close()

        return tables_list

