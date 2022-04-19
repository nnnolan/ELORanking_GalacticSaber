import mysql.connector
from mysql.connector import errorcode
import add_data_test, tables, query_data_test

config = {
  'user': 'root',
  'password': 'password',
  'host': '127.0.0.1',
  'database': 'employees',
  'raise_on_warnings': True
}

try:
    connection = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = connection.cursor()
    tables.build_tables(cursor, connection)
    add_data_test.add_data(cursor, connection)
    query_data_test.query_tables(cursor)
    cursor.close()
    connection.close()
