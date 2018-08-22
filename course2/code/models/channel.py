import sqlite3


class ChannelModel:

    def __init__(self, _id, name):
        self.id = _id
        self.name = name


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM channels where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            channel = cls(*row)

        else:
            channel = None

        connection.close()
        return channel

    @classmethod
    def fing_id_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT channel_id FROM channels where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()
        if row:
            return {"channel_id": row[0]}
        return {"channel_id": None}


    @classmethod
    def find_by_id(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM channels where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        print(row)
        if row:
            channel = cls(*row)
            print(channel)
        else:
            channel = None

        connection.close()
        return channel

    @classmethod
    def get_channel_name_by_id(cls, channel_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = """SELECT name FROM channels where channel_id=?"""
        result = cursor.execute(query, (channel_id,))
        row = result.fetchone()

        if row:
            channel = cls(*row)
        else:
            channel = None

        connection.close()
        return channel
