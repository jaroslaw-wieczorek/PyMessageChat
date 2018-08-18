import sqlite3

connection = sqlite3.connect('data.db')


cursor = connection.cursor()
create_table = """
                CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                      user_id text unique,
                                      email text unique,
                                      username text,
                                      password text)
               """

cursor.execute(create_table)

user = ('hfhs9fh987', 'jose@jose.pl', 'jose', 'asdf')

insert_query = 'INSERT INTO users(user_id, email, username, password) values(?, ?, ?, ?)'
cursor.execute(insert_query, user)

users = [
    ('123iirwe', 'bob@dodo.pl', 'bob', '1234'),
    ('49349545', 'bob@dodo.pl', 'jon', '1234'),
    ('7384934d', 'bob@dodo.pl', 'sun', '1234')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
