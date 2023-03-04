import sqlite3
import os
# Creating connect to db
# Here we have just a file of db

#Getting absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Chinook_Sqlite.sqlite")

conn = sqlite3.connect(db_path)

#Example of connecting to PostgreSQL db using psycopg2 library
#conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database)


# Creating cursor - special object that makes requests and gives us answers
cursor = conn.cursor()

# Working with db
# Making SELECT request to db, using usual SQL-syntax

cursor.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")

# Getting result of request
results = cursor.fetchall()
results2 =  cursor.fetchall() # here we have nothing, because we`ve already fetched the result, so cursor is empty now

#print(results)   # [('A Cor Do Som',), ('Aaron Copland & London Symphony Orchestra',), ('Aaron Goldberg',)]
#print(results2)  # []

# Making INSERT request to db, using usual SQL-syntax
cursor.execute("insert into Artist values (Null, 'A Aagrh!') ")

# We have to commit transaction in order to save info
conn.commit()

# Проверяем результат
cursor.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")
results = cursor.fetchall()
print(results)

# splitting the request on multiple lines using '''
#cursor.execute("""
#  SELECT name
#  FROM Artist
#  ORDER BY Name LIMIT 3
#""")

# Making several requests in one method
#cursor.executescript("""
# insert into Artist values (Null, 'A Aagrh!');
# insert into Artist values (Null, 'A Aagrh-2!');
#""")

# substitution an element using second parameter of execute method
# in PostgreSQL and MySql we use %s instead of ?
#cursor.execute("SELECT Name FROM Artist ORDER BY Name LIMIT ?", ('2'))

# using named substitute
#cursor.execute("SELECT Name from Artist ORDER BY Name LIMIT :limit", {"limit": 3})


# Even if we give one value - we have to use tuple. So that why we write , in the end of tuple
new_artists = [
    ('A Aagrh!',),
    ('A Aagrh!-2',),
    ('A Aagrh!-3',),
]
# Giving many values using executemany and list of tuples   
cursor.executemany("insert into Artist values (Null, ?);", new_artists)

# fetching info from request one by one using fetchone. If fetch is empty - always returns None
cursor.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")
print(cursor.fetchone())    # ('A Cor Do Som',)
print(cursor.fetchone())    # ('Aaron Copland & London Symphony Orchestra',)
print(cursor.fetchone())    # ('Aaron Goldberg',)
print(cursor.fetchone())    # None


# Iterating cursor
for row in cursor.execute('SELECT Name from Artist ORDER BY Name LIMIT 3'):
        print(row)

# Creating good code that is more stable to errors while inserting
# While inserting database locks for other connections until we made commit or rollback method
try:
    cursor.execute("insert into Artist values (Null, 'A Aagrh!') ")
    result = cursor.fetchall()
except sqlite3.DatabaseError as err:       
    print("Error: ", err)
else:
    conn.commit()
# closing db. We can use with: too 
conn.close()