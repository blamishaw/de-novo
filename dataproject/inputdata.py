""" Program to input data into a MySQL table wrapped in class InputData

    The table is dynamic so theoretically we can input data from a variable number
    of web scrapers and the table will adjust it's columns and values appropriately.

    The database is structured in this way:
        TABLE "names":
            COLUMNS: "ID" INT AUTO_INCREMENT PRIMARY KEY, "Name" TEXT
        TABLE "data":
            COLUMNS: "ID" INT, other columns are variable as the table dynamically expands
        TABLE "areas":
            COLUMNS "ID" INT, other columns are variable as the table dynamically expands

"""

import re

from driver import connect_to_database
from helper import *

mydb = connect_to_database()

class InputData:
    """ Class that inputs data into tables in database
        Use this class if you don't need to query database prior to input """

    def __init__(self, table, allow_multiple=False):
        self._table = table
        self._cursor = mydb.cursor(buffered=True)
        self.allow_multiple = allow_multiple

    def check_column_exists(self, title, datatype):
        """ Checks if a column exists in the table """

        query = f"SHOW COLUMNS FROM {self._table} LIKE %s;"
        self._cursor.execute(query, (title,))
        col = self._cursor.fetchone()

        if col is None and title != "Name":
            self.add_column(title, datatype)
            print(f"Column added with name: {title} and datatype: {datatype} in table: {self._table}.")

    def add_column(self, title, datatype):
        """ Adds a column to the table """

        query = f"ALTER TABLE {self._table} ADD COLUMN {title} {datatype};"
        self._cursor.execute(query)

    def process_columns(self, firm_list):
        """ Processes whether or not to add columns to table
            :rtype List[names of columns in table] """

        if len(firm_list) == 0:
            raise Exception("Empty List")

        columns = []
        for key, value in firm_list[0].items():
            title = key[0].upper() + key[1:]
            if isinstance(value, str):
                datatype = 'TEXT'
            elif isinstance(value, float):
                datatype = 'FLOAT'
            else:
                datatype = 'INT'
            self.check_column_exists(title, datatype)
            columns.append(title)
        return columns

    def fuzzy_match_name(self, name):
        """ This processes firm name and attempts to find a match in the database
            :rtype string/None -> the shortened, processed name of the firm used for querying"""

        table = 'names'

        name = remove_multiple(name, [',', ' LLP', ' PC'])                           # remove these characters
        name = remove_after_parens(name).replace("’", "'")                           # replace weird apostrophes
        name = re.sub(' +', ' ', name)                                               # remove double spacing

        """ This is for a single firm: Gordon Rees Scully Matsukhani LLP"""
        if name[0] == ' ':
            name = name[1:]                                                          # remove whitespace at the front

        if len(name) > 12:
            name = name[:12]

        query = f"SELECT ID, Name FROM {table} WHERE Name LIKE %s;"
        self._cursor.execute(query, (name + "%",))
        row = self._cursor.fetchone()

        if row is None:
            return None
        return name

    def get_name_id(self, name):
        """ Returns the ID of a firm name if it exists in table 'names'
            If it does not, it insert the name into table and returns ID
        """

        table = 'names'

        result = self.fuzzy_match_name(name)

        if result is None:
            result = name.replace(',', '')

            query1 = f"INSERT INTO {table} (Name) VALUES (%s);"
            self._cursor.execute(query1, (result,))
            mydb.commit()

        query2 = f"SELECT ID FROM {table} WHERE Name LIKE (%s);"
        self._cursor.execute(query2, (result+'%',))
        mydb.commit()

        id = self._cursor.fetchone()

        return id[0]

    def insert_data(self, firm_list, columns):
        """ If name exists in table -> update appropriate column values
            If name does not exist -> insert new row and update columns """

        for item in firm_list:
            values = list(item.values())

            id = self.get_name_id(values[0])

            if not self.allow_multiple:
                query1 = f"SELECT * FROM {self._table} WHERE ID=%s;"
                self._cursor.execute(query1, (id,))
                mydb.commit()
                row = self._cursor.fetchone()

                if row is None:
                    query2 = f"INSERT INTO {self._table} (ID) VALUES (%s);"
                    self._cursor.execute(query2, (id,))
                    mydb.commit()


                for i in range(1, len(columns)):
                    query3 = f"UPDATE {self._table} SET {columns[i]}=%s WHERE ID=%s AND {columns[i]} IS NULL;"
                    self._cursor.execute(query3, (values[i], id))
                    mydb.commit()

            else:
                query3 = f"INSERT INTO {self._table} (ID, {columns[1]}, {columns[2]}, {columns[3]}) " \
                    f"  VALUES (%s, %s, %s, %s);"
                self._cursor.execute(query3, (id, values[1], values[2], values[3]))
                mydb.commit()

    def push(self, firms_list):
        """ Driver function to process columns and add data to table """

        cols = self.process_columns(firms_list)
        self.insert_data(firms_list, cols)

    def change_table(self, table):
        self._table = table

    def check_overlap(self):
        """ This has to be updated manually everytime a table is added
            Prints the overlap of the tables (i.e. the number of rich entries)
        """

        tables = ['names', 'data', 'areas', 'acquired']

        query1 = f"""SELECT COUNT(*)
                        FROM {tables[0]} AS n
                        JOIN {tables[1]} AS d ON n.ID = d.ID
                        JOIN {tables[2]} AS a ON n.ID = a.ID
                        JOIN {tables[3]} AS ac ON n.ID = ac.ID
                        ;"""
        self._cursor.execute(query1)
        mydb.commit()

        ans1 = self._cursor.fetchone()
        ans1 = ans1[0]

        query2 = f"SELECT COUNT(*) FROM names;"
        self._cursor.execute(query2)
        mydb.commit()

        ans2 = self._cursor.fetchone()
        ans2 = ans2[0]

        print("Rich Entry Percentage:", round((ans1/ans2) * 100, 2), "%")

    def close(self):
        self._cursor.close()

