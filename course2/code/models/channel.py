import sqlite3


class ChannelModel:

    def __init__(self, _channel_id, name):
        self.channel_id = _channel_id
        self.name = name

    def json(self):
        return {'channel_id': self.channel_id, 'name': self.name}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM channels where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)
        else:
            return None

    @classmethod
    def find_id_by_name(cls, name):
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
    
    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO channels VALUES(null, ?)"
        cursor.execute(query, (self.name, ))

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE channels SET name=? WHERE channel_id=?"

        cursor.execute(query, (self.name, self.channel_id))

        connection.commit()
        connection.close()
