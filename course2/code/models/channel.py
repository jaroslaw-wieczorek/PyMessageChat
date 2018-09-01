from db import db


class ChannelModel(db.Model):

    __tablename__ = 'channels'

    channel_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), unique=True)
    owners = db.Column(db.Binary)
    users = db.Column(db.Binary)

    def __init__(self, _channel_id, name, owners, users):
        self.channel_id = _channel_id
        self.name = name
        self.owners = owners
        self.users = users

    def json(self):
        return {
            'channel_id': self.channel_id,
            'name': self.name,
            'owners': self.owners,
            'users': self.users
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # SELECT * FROM items WHERE name=name

    """
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
            """

    @classmethod
    def find_id_by_name(cls, name):
        return cls.query.filter_by(name=name).channel_id
    """
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
    """

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(channel_id=_id)
    """
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

        query = "SELECT name FROM channels where channel_id=?"
        result = cursor.execute(query, (channel_id,))
        row = result.fetchone()

        if row:
            channel = cls(*row)
        else:
            channel = None

        connection.close()
        return channel
    """
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    """
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
    """

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
