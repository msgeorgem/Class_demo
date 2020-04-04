#https://www.psycopg.org/docs/usage.html
import psycopg2

connection = psycopg2.connect('dbname=first_data_base user=geo', password='1234', host="127.0.0.1", port="5432")

cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS table2;')

cursor.execute('''
  CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
''')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))

SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'

data = {
  'id': 2,
  'completed': False
}
cursor.execute(SQL, data)
data = {
  'id': 3,
  'completed': False
}
cursor.execute(SQL, data)

cursor.execute('SELECT * from table2;')
result = cursor.fetchall()
##result = cursor.fetchone()
print('fetchmany', result)

cursor.execute('SELECT * from table2;')
result1 = cursor.fetchmany(2)
print('fetchmany', result1)

connection.commit()

connection.close()
cursor.close()

