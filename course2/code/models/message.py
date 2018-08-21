import sqlite3


class MessageModel:
    def __init__(self, _id, _channel_id, content, time, user_id):
        self.id = _id
        self.content = content
        self.time = time
        self.channel_id = _channel_id
        self.user_id = user_id

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
    def find_by_id(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT * FROM messages where name=?"""
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            channel = cls(*row)
        else:
            channel = None

        connection.close()
        return channel
