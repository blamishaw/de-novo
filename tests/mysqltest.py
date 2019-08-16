import mysql.connector
import csv


mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='denovosql',
    database='my_database'
)

cursor = mydb.cursor()


# with open('/Users/brendanlamishaw/Desktop/firms.csv') as file:
#     for i, x in enumerate(csv.reader(file, delimiter=",")):
#         if 216 > i > 0:
#             values = (x[1], x[2], x[3], x[4], i)
#             cursor.execute("""UPDATE firms SET InsiderRating= %s,
#                                                IndustryRep= %s,
#                                                LikedPercent= %s,
#                                                Website= %s
#
#                              WHERE ID= %s;""", values)

name = 'Adams'

query = "SELECT * FROM test WHERE Name LIKE %s;"
cursor.execute(query, (f'{name}%',))

print(len(tuple(cursor)))


# mydb.commit()

cursor.close()
mydb.close()

