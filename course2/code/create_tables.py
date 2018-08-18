import sqlite3
from datetime import date, datetime

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#create_table = """CREATE TABLE IF NOT EXISTS users (
#						id INTEGER PRIMARY KEY AUTOINCREMENT, 
#						email text, 
#						username text, 
#						password text);
#			   """


create_table_users = """	CREATE TABLE users (
						user_id integer PRIMARY KEY AUTOINCREMENT,
						username text, 
						password text,
						email text, 
						picture text, 
						status text);
					"""

create_table_channels = """ CREATE TABLE channels (
							channel_id integer PRIMARY KEY AUTOINCREMENT,
							name text);
						"""

create_table_messages = """	CREATE TABLE messages (
							message_id integer PRIMARY KEY AUTOINCREMENT,
							contents text,
							time datetime,
							channel_id integer, 
							user_id integer, 
							FOREIGN KEY(channel_id) REFERENCES channels(channel_id),
							FOREIGN KEY(user_id) REFERENCES users(user_id));
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

create_channel = """ INSERT INTO channels values(null, 'kanal_1');"""
cursor.execute(create_channel)

now = datetime.now()
create_message = """ INSERT INTO messages values(null, 'treść pierwszej testowej wiadomości', ?, 1, 1);"""
cursor.execute(create_message, (now,))

create_table_channels_users = """ INSERT INTO channels_users values(1,1)"""
cursor.execute(create_table_channels_users)

connection.commit()

connection.close()

