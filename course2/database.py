import sqlite3

connection = sqlite3.connect('data.db')


cursor = connection.cursor()
create_table = """
                CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                      email text unique,
                                      username text,
                                      password text)
               """

cursor.execute(create_table)

user = ('jose@jose.pl', 'jose', 'asdf')

insert_query = 'INSERT INTO users(user_id, email, username, password) values(?, ?, ?)'
cursor.execute(insert_query, user)

users = [
    ('bob@dodo.pl', 'bob', '1234'),
    ('bob@dodo.pl', 'jon', '1234'),
    ('bob@dodo.pl', 'sun', '1234')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
