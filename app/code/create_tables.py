import sqlite3
import json
from datetime import date, datetime

connection = sqlite3.connect('data.db')
cursor = connection.cursor()



create_table_users = """CREATE TABLE users (
						id text,
						username text, 
						password text,
						email text, 
						avatar text, 
						status text);
					"""

create_table_channels = """ CREATE TABLE channels (
							channel_id text,
							name text,
							owners text,
							users text)
						"""

create_table_messages = """CREATE TABLE messages (
							message_id text,
							channel_id text, 
							content text,
							time datetime,
							username text, 
							avatar text);
						"""



cursor.execute(create_table_users)
cursor.execute(create_table_channels)
cursor.execute(create_table_messages)

#create_user = """ INSERT INTO users values("fdf", 'jaro', '1234', 'jaroslaw.wieczorek@sealcode.org', 'None', 'offline');"""
$cursor.execute(create_user)

json_users = ["jaro", "bob"]

json_users_dump = json.dumps(json_users)


json_owners = ["jaro", "bob"]


json_owners_dump = json.dumps(json_owners)

print(json_owners_dump)


create_channel = """ INSERT INTO channels values(?, ?, ?, ?);"""
cursor.execute(create_channel, ("nnsugn", "kanal_1", json_owners_dump, json_users_dump))

now = datetime.now()
create_message = """ INSERT INTO messages values("fdfb", 1, 'treść pierwszej testowej wiadomości', ?, 1, "avatar");"""
cursor.execute(create_message, (str(now),))


now = datetime.now()
create_message = """ INSERT INTO messages values("fgfgj9", 1, 'treść pierwszej testowej wiadomości', ?, 1, "avatar");"""
cursor.execute(create_message, (str(now),))

connection.commit()
connection.close()

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

select_messages_query = """ SELECT * FROM messages WHERE channel_id =? """
data = cursor.execute(select_messages_query, (1,))
rows = data.fetchall()
print(rows)
