import pyodbc
import locale
import sqlserverport
locale.resetlocale()
# conn = pyodbc.connect('DRIVER=ODBC Driver 13 for SQL Server;SERVER={};...'.format(serverspec))

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=db.webteach.iu.edu,1433;'
                      'Database=asmpatel_1763816;')

cursor = connection.cursor()
cursor.execute('SELECT * FROM CLIENT_DATA')

for row in cursor:
    print(row)
