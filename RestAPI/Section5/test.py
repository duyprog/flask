import sqlite3

connection = sqlite3.connect('data.db')
 
cursor = connection.cursor() # allow us to choose thing to start, choose database this is response for executing queries

# Create table 
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'duy', 'asf')


insert_query = "INSERT INTO users VALUES(?, ?, ?)"
cursor.execute(insert_query, user)

users= [
    (2, 'y', 'abc'),
    (3, 'd', '213')
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

cursor.execute(select_query)

connection.commit()

connection.close()
