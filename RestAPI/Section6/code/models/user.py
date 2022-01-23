import sqlite3
class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))  # param must be a tuple
        row = result.fetchone()  # get the first row of result set
        if row:
            user = UserModel(row[0], row[1], row[2])  # first column, second, third
        else:
            user = None

        connection.close()  # if add any data we need to commit
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?" 
        result = cursor.execute(query, (_id,)) # param must be a tuple 
        row = result.fetchone() # get the first row of result set 
        if row: 
            user = UserModel(row[0], row[1], row[2]) # first column, second, third 
        else: 
            user = None 
        
        connection.close() # if add any data we need to commit 
        return user