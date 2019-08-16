from driver import connect_to_database

mydb = connect_to_database()

class ReadData:
    """ Class to read data from MySQL database """

    def __init__(self):
        self._cursor = mydb.cursor(buffered=True)

    def get_all_names(self):
        """ :rtype List[all ID-name pairs in database from table 'names']

            This is used when scraping from news aggregation sites
        """

        names = []

        table = 'names'
        query = f"SELECT ID, Name FROM {table};"
        self._cursor.execute(query)
        mydb.commit()

        result = self._cursor.fetchall()
        for ID, Name in result:
            names.append((ID, Name))

        return names
