import sqlite3


class MessageModel:
    def __init__(self, _message_id, _channel_id, content, time, username, avatar):
        self.message_id = _message_id
        self.channel_id = channel_id
        self.content = content
        self.time = time
        self.username = username
        self.avatar = avatar

    def json(self):
        return {"message_id": self.message_id,
                "channel_id": self.channel_id,
                "content": self.content,
                "time": self.time,
                "user_name": self.user_name
                }

    @classmethod
    def find_by_word(cls, word):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM messages WHERE content LIKE '%?%'"""
        result = cursor.execute(query, (word,))
        row = result.fetchone()

        if row:
            channel = cls(*row)
        else:
            channel = None

        connection.close()
        return channel

    @classmethod
    def find_by_id(cls, channel_id, message_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM messages where channel_id=? and message_id=?"
        result = cursor.execute(query, (channel_id, message_id))
        row = result.fetchone()

        if row:
            channel = cls(*row)
        else:
            channel = None

        connection.close()
        return channel

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO messages VALUES(null, ?, ?, ?, ?, ?)"
        cursor.execute(query, (self.channel_id, self.content,
                               self.time, self.username, self.avatar))

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE messages SET content=? and avatar=? WHERE channel_id=? AND message_id=?"
        cursor.execute(query, (self.content, self.avatar, self.channel_id, self.message_id))

        connection.commit()
        connection.close()