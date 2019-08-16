""" Database models used to retrieve data from the MySQL source
    Django largely implemented these for me using the inspectdb method
    although I did add some raw SQL queries of my own in the 'Names' class
"""


from django.db import models
from django.db import connection, transaction



class Acquired(models.Model):
    id = models.IntegerField(db_column='ID',primary_key=True)  # Field name made lowercase.
    acquired = models.TextField(db_column='Acquired', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'acquired'


class Areas(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    mainareas = models.TextField(db_column='MainAreas', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'areas'


class Data(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    city = models.TextField(db_column='City', blank=True, null=True)  # Field name made lowercase.
    attorneys = models.TextField(db_column='Attorneys', blank=True, null=True)  # Field name made lowercase.
    growth = models.FloatField(db_column='Growth', blank=True, null=True)  # Field name made lowercase.
    revenue = models.TextField(db_column='Revenue', blank=True, null=True)  # Field name made lowercase.
    country = models.TextField(db_column='Country', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'data'


class Names(models.Model):
    cursor = connection.cursor()

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name')  # Field name made lowercase.

    def get_data(self):
        query = """SELECT data.city as city, data.attorneys as attorneys, data.growth as growth, data.revenue as revenue, data.country as country
                    FROM data WHERE ID=%s;"""
        self.cursor.execute(query, (self.id,))
        transaction.commit()

        result = self.cursor.fetchone()

        if result is None:
            return ('NULL', 'NULL','NULL', 'NULL', 'NULL',)

        return result

    def get_news(self):
        query = """SELECT headline, link FROM news WHERE ID=%s"""
        self.cursor.execute(query, (self.id,))
        transaction.commit()

        result = self.cursor.fetchall()

        if result:
            return result
        return 'None'

    def get_main_areas(self):
        query = "SELECT MainAreas FROM areas WHERE ID=%s;"
        self.cursor.execute(query, (self.id,))
        transaction.commit()

        result = self.cursor.fetchone()

        return result

    def search_query(self, search_query):
        query = "SELECT names.Name FROM names JOIN data ON data.ID = names.ID WHERE Name LIKE %s OR data.City LIKE %s;"

        self.cursor.execute(query, ('%'+search_query+'%', '%'+search_query+'%'))
        transaction.commit()

        result = self.cursor.fetchall()

        return [name[0] for name in result]

    def __str__(self):
        return self.name


    class Meta:
        ordering = ["name"]
        managed = False
        db_table = 'names'


class News(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    headline = models.TextField(db_column='Headline', blank=True, null=True)  # Field name made lowercase.
    link = models.TextField(db_column='Link', blank=True, null=True)  # Field name made lowercase.
    time_posted = models.TextField(db_column='Time_posted', blank=True, null=True)  # Field name made lowercase.
    source = models.TextField()

    class Meta:
        managed = False
        db_table = 'news'


class TestLog(models.Model):
    stamp = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_log'