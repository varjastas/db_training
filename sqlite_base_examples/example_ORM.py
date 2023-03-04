# Importing ORM library. 
from peewee import *
import os

# Connecting to bd
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Chinook_Sqlite.sqlite")
conn = SqliteDatabase(db_path)


#Creating models

# Creating base model, from wich all derived classes will derive
class BaseModel(Model):
    class Meta:
        database = conn


# Creating artist model
class Artist(BaseModel):
    artist_id = AutoField(column_name='ArtistId')
    name = TextField(column_name='Name', null=True)

    class Meta:
        table_name = 'Artist'


def print_last_five_artists():
    """ Printing last five rows in table Artist"""
    print('########################################################')
    cur_query = Artist.select().limit(5).order_by(Artist.artist_id.desc())
    for item in cur_query.dicts().execute():
        print('artist: ', item)


# Creating cursor
cursor = conn.cursor()

#Using cursor

# Making select request to db using SQL-syntax
cursor.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")

#  Getting full result
results = cursor.fetchall()
print(results)   # [('A Cor Do Som',), ('AC/DC',), ('Aaron Copland & London Symphony Orchestra',)]


#READ

# Get one row using get
artist = Artist.get(Artist.artist_id == 1)

#Now we have artist row and we can manipulate with it(update, delete, read)
print('artist: ', artist.artist_id, artist.name)  # artist:  1 AC/DC


# Creating request using select
query = Artist.select()
print(query)
# SELECT "t1"."ArtistId", "t1"."Name" FROM "Artist" AS "t1"

#Adding additional methods
query = Artist.select().where(Artist.artist_id < 10).\
                        limit(5).order_by(Artist.artist_id.desc())
print(query)
# SELECT "t1"."ArtistId", "t1"."Name" FROM "Artist" AS "t1"
#   WHERE ("t1"."ArtistId" < 10) ORDER BY "t1"."ArtistId" DESC LIMIT 5

# Now we can get rows from our query. 
artists_selected = query.dicts().execute()
print(artists_selected)
# <peewee.ModelDictCursorWrapper object at 0x7f6fdd9bdda0>
# Creating iterator on result 
for artist in artists_selected:
    print('artist: ', artist)   # artist:  {'artist_id': 9, 'name': 'BackBeat'}
   


################  CREATE  #######################

# Using create and giving all info in create method
Artist.create(name='1-Qwerty')

# Creating new object, then manipulating its fields and then save
artist = Artist(name='2-asdfg')
artist.save()  # save() returns the number of rows modified.

# Adding many rows by one by creating list of dicts.
artists_data = [{'name': '3-qaswed'}, {'name': '4-yhnbgt'}]
Artist.insert_many(artists_data).execute() # REQUIRES EXECUTE!

# Checking that all is good
print_last_five_artists()
# artist:  {'artist_id': 279, 'name': '4-yhnbgt'}
# artist:  {'artist_id': 278, 'name': '3-qaswed'}
# artist:  {'artist_id': 277, 'name': '2-asdfg'}
# artist:  {'artist_id': 276, 'name': '1-Qwerty'}
# artist:  {'artist_id': 275, 'name': 'Philip Glass Ensemble'}


############### Update ##############

#Creating artist
artist = Artist(name='2-asdfg+++++')
#Updating its id(does not work with AutoField) artist.artist_id = 277  
artist.save()

print_last_five_artists()
# artist:  {'artist_id': 279, 'name': '4-yhnbgt'}
# artist:  {'artist_id': 278, 'name': '3-qaswed'}
# artist:  {'artist_id': 277, 'name': '2-asdfg+++++'}
# artist:  {'artist_id': 276, 'name': '1-Qwerty'}
# artist:  {'artist_id': 275, 'name': 'Philip Glass Ensemble'}

#Updating many queries using method update.
#in parameters we set what to update 
# in where we filter which rows will be updated
query = Artist.update(name=Artist.name + '!!!').where(Artist.artist_id > 275)
query.execute()

print_last_five_artists()
# artist:  {'artist_id': 279, 'name': '4-yhnbgt!!!'}
# artist:  {'artist_id': 278, 'name': '3-qaswed!!!'}
# artist:  {'artist_id': 277, 'name': '2-asdfg+++!!!'}
# artist:  {'artist_id': 276, 'name': '1-Qwerty!!!'}
# artist:  {'artist_id': 275, 'name': 'Philip Glass Ensemble'}


###################### Deleting #######################

# Getting row by get method
artist = Artist.get(Artist.artist_id == 279)
# deleting using delete_instance on artist object
artist.delete_instance()

print_last_five_artists()
# artist:  {'artist_id': 278, 'name': '3-qaswed!!!'}
# artist:  {'artist_id': 277, 'name': '2-asdfg+++!!!'}
# artist:  {'artist_id': 276, 'name': '1-Qwerty!!!'}
# artist:  {'artist_id': 275, 'name': 'Philip Glass Ensemble'}
# artist:  {'artist_id': 274, 'name': 'Nash Ensemble'}

# Deleting many rows at once using delete and specifying by delete
query = Artist.delete().where(Artist.artist_id > 275)
query.execute()

print_last_five_artists()
# artist:  {'artist_id': 275, 'name': 'Philip Glass Ensemble'}
# artist:  {'artist_id': 274, 'name': 'Nash Ensemble'}
# artist:  {'artist_id': 273, 'name': 'C. Monteverdi, Nigel Rogers - Chiaroscuro; London Baroque; London Cornett & Sackbu'}
# artist:  {'artist_id': 272, 'name': 'Emerson String Quartet'}
# artist:  {'artist_id': 271, 'name': 'Mela Tenenbaum, Pro Musica Prague & Richard Kapp'}


# Не забываем закрыть соединение с базой данных в конце работы
conn.close()