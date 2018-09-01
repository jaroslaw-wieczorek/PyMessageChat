import sqlite3
import json
from datetime import date, datetime

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#create_table = """CREATE TABLE IF NOT EXISTS users (
#						id INTEGER PRIMARY KEY AUTOINCREMENT, 
#						email text, 
#						username text, 
#						password text);
#			   """


create_table_users = """CREATE TABLE users (
						user_id integer PRIMARY KEY AUTOINCREMENT,
						username text, 
						password text,
						email text, 
						avatar text, 
						status text);
					"""

create_table_channels = """ CREATE TABLE channels (
							channel_id integer PRIMARY KEY AUTOINCREMENT,
							name text,
							owners text,
							users text)
						"""

create_table_messages = """CREATE TABLE messages (
							message_id integer PRIMARY KEY AUTOINCREMENT,
							channel_id integer, 
							content text,
							time datetime,
							username integer, 
							avatar text,
							FOREIGN KEY(channel_id) REFERENCES channels(channel_id));
						"""


create_table_channels_users = """ CREATE TABLE channels_users (
								  channel_id integer,
								  user_id integer,
								  FOREIGN KEY(channel_id) REFERENCES channels(channel_id),
								  FOREIGN KEY(user_id) REFERENCES users(user_id));
							  """


cursor.execute(create_table_users)
cursor.execute(create_table_channels)
cursor.execute(create_table_messages)
cursor.execute(create_table_channels_users)


create_user = """ INSERT INTO users values(null, 'jaro', '1234', 'jaroslaw.wieczorek@sealcode.org', 'None', 'offline');"""
cursor.execute(create_user)

json_users = ["jaro", "bob"]

json_users_dump = json.dumps(json_users)


json_owners = ["jaro", "bob"]


json_owners_dump = json.dumps(json_owners)

print(json_owners_dump)


create_channel = """ INSERT INTO channels values(null, ?, ?, ?);"""
cursor.execute(create_channel, ("kanal_1", json_owners_dump, json_users_dump))

now = datetime.now()
create_message = """ INSERT INTO messages values(null, 1, 'treść pierwszej testowej wiadomości', ?, 1, "avatar");"""
cursor.execute(create_message, (str(now),))


now = datetime.now()
create_message = """ INSERT INTO messages values(null, 1, 'treść drugiej testowej wiadomości', ?, 1, "avatar");"""
cursor.execute(create_message, (str(now),))

create_table_channels_users = """ INSERT INTO channels_users values(1,1)"""
cursor.execute(create_table_channels_users)

connection.commit()
connection.close()

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

select_messages_query = """ SELECT * FROM messages WHERE channel_id =? """
data = cursor.execute(select_messages_query, (1,))
rows = data.fetchall()
print(rows)
