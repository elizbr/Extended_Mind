

#imports
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import spotipy
import spotipy.util as util
import secrets
import requests
from bs4 import BeautifulSoup
import lxml
import pitchfork
import sqlite3

#reference
# https://github.com/michalczaplinski/pitchfork


"""
export SPOTIPY_CLIENT_ID = secrets.spotify_id
export SPOTIPY_CLIENT_SECRET= secrets.spotify_secret
export SPOTIPY_REDIRECT_URI= 'http://localhost/?code='

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

util.prompt_for_user_token(username = secrets.spotify_nm,
                           scope = 'user-read-private',
                           client_id= SPOTIPY_CLIENT_ID,
                           client_secret= SPOTIPY_CLIENT_SECRET,
                           redirect_uri='http://localhost/?code=')


#scrape spotify for artist 
def get_artist(name):
    '''borrowed code; 
    '''
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None
"""

#scrape pitchfork for album reviews 


#scrape spotify with cache


#album query string from spotify to pitchfork
def format_album_query(album):
    '''takes string album and formats into query string
    parameter <str> - sentence case album title 
    return <str> - formatted query string
    '''
    try: 
        query = ''
        if ' ' in album.strip():
            step_one = album.lower().split(' ')
            for word in step_one:
                query = query + '%20' + word
        else:
            query = album.lower()
    except:
        query = album.lower()
    return f"https://pitchfork.com/search/?query={query}"

'''
#
'''
#scrape pitchfork with cache 


# create dbs


#1. Create the database and its tables
def create_db():
    conn = sqlite3.connect('albums.sqlite')
    cur = conn.cursor()
    #drop_bars_sql = 'DROP TABLE IF EXISTS "Bars"'
    #drop_countries_sql = 'DROP TABLE IF EXISTS "Countries"'

    create_album_sql = '''
        CREATE TABLE IF NOT EXISTS "Albums" (
	    "Id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	    "AlbumTitle"	TEXT UNIQUE,
	    "AlbumLabel"	TEXT,
	    "AlbumEditorial"	TEXT UNIQUE,
	    "AlbumCover"	TEXT UNIQUE,
        "Year"      TEXT,
	    "AlbumScore"	NUMERIC,
	    "ArtistTitle"	TEXT)
        '''

    create_artist_sql = '''
        CREATE TABLE IF NOT EXISTS "Artists" (
	    "Id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	    "ArtistTitle"	TEXT UNIQUE,
	    "ArtistGenre"	TEXT,
	    "ArtistBio"	TEXT UNIQUE,
	    "TopAlbum"	TEXT UNIQUE,
	    "TopTrack"	NUMERIC,
	    "AlbumList"	INTEGER)
        '''

    #cur.execute(drop_bars_sql)
    #cur.execute(drop_countries_sql)

    cur.execute(create_artist_sql)
    cur.execute(create_album_sql)

    conn.commit()
    conn.close()


#2. Extract data records from the CSV and Web API. 
def album_scrape_p(artist, album):
    '''takes artist and album and creates dict for each 
    album available on pitchfork 
    Parameters:
    _artist <str> - Artist Name
    _album <album name> - Artist's specificed album 
    Returns:
    _album_content <list> - contains all info 
    necessary for db add 
    '''
    p = pitchfork.search(artist, album) # the title is autocompleted
    album = p.album() # the full album title
    label = p.label()
    editorial = p.editorial()
    score = p.score()
    artist = p.artist()
    year = p.year()
    try: 
        cover = p.cover()
    except:
        cover = 'None'
    album_content = (album, label, editorial, cover, year, score, artist,)
    return album_content



#3. Insert each extracted record into the DB, making sure that the 
#relationships between Bars and Countries are correctly represented.
def add_album_to_sql(cont):
    try:
        conn = sqlite3.connect('albums.sqlite')
        cur = conn.cursor()
        print("Successfully Connected to SQLite")

        insert_query = f"""INSERT INTO Albums
        (AlbumTitle, AlbumLabel, AlbumEditorial, AlbumCover, Year, AlbumScore, ArtistTitle) 
        VALUES {cont}"""

        cur.execute(insert_query)
        conn.commit()
        print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
        cur.close()

    except:
        print("Failed to insert data into sqlite table")
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")



#assign album info to album.sql 


#assign artist info to artist.sql


# User input for artist 


#flask interfact for user 

################
create_db()
v = album_scrape_p('Deafheaven', 'Sunbather')
#print(v)
xxx = ('High Violet', '4AD', 
'''The National became popular in a very traditional way: 
by releasing some really good albums, then touring the hell out of them. 
They\'re boilerplate indie, free of hot new genre tags or feature-ready 
backstories, which is something their detractors derive great joy from 
pointing out. If the National are important, rather than merely good, 
it\'s for writing about the type of lived-in moments that rock bands 
usually don\'t write about that well. The characters in National songs 
have real jobs, have uninteresting sex, get drunk, and lie to one another. 
They do so during the regular course of a workaday week, on Tuesdays and 
Wednesdays. The National aren\'t "dad-rock" so much as "men\'s magazine 
rock": music chiefly interested in the complications of being a stable 
person expected to own certain things and dress certain ways.\nOn the Nat
ional\'s fifth album, High Violet, those constraints are starting to wear
 on them, which makes a lot of sense: they wear on most people. In betwee
 n patches of obtuse imagery, singer Matt Berninger sounds increasingly s
 elf-destructive. The record\'s upbeat numbers don\'t cheer him up so muc
 h as commiserate with him. All of this makes High Violet a dark affair, 
 even for a band with a reputation for sad-bastard melodrama. The National
 ve never sounded triumphant, but they can still be reassuring, with Be
 rninger\'s\xa0lyrics acting as salves for our own neuroses. Six drink
 s in, tired of your coworkers, wishing you could just go home and lau
 gh at sitcoms with someone? Maybe get laid? The National\'s got your
  back.\nWith an ever rising profile and plenty of indie-famous friends-
  - Sufjan Stevens and Bon Iver\'s Justin Vernon guest here-- the Nat
  ional were afforded the opportunity to obsess over High Violet. They c
  ould\'ve holed up and recorded an idiosyncratic, expectation-defying mes
  s. Instead they produced an ornate, fussed-over record that sounds like 
  no one other than themselves. Given the amount of flack they take for b
  eing a no-frills bore, simply refining their sound was arguably the brav
  er option. They miss, occasionally-- the string-drenched closer, "Vande
  rlyle Crybaby Geeks", is too decadent for its own good-- but mostly, t
  hey construct gorgeous, structurally sound vignettes. There are few b
  ands that could craft a song like "Sorrow"-- in which emotion acts as 
  a character and the band turns Berninger\'s balladry into a well paced 
  jog-- without stumbling over their own ambitions. The guitars on "Afra
  id of Everyone" actually sound nervous; "England" speaks of cathedral
  s over properly magisterial drums. These are triumphs of form.\nBernin
  ger is still, for the most part, a socially obsessed claustrophobe. He 
  has upper-class guilt on "Lemonworld" ("Cousins and cousins somewhere o
  verseas/ But it\'ll take a better war to kill a college man like me," "T
  his pricey stuff makes me dizzy"). "Bloodbuzz Ohio"\'s magnificent choru
  s ("I still owe money/ To the money/ To the money I owe") addresses the 
  familiar, harrowing financial burdens of adulthood. He\'s best when he t
  ones down the angst in favor of reflection or confusion. High Violet see
  ms less likely to engender the personal connections of Boxer, but it\'s 
  also bigger and more engaging-- a possibly offputting combination for a 
   band following the footsteps of Echo and the Bunnymen, Wilco, and Arcad
   e Fire. After all, eagerness often trumps execution, and the National a
   ren\'t immune: For his part, Berninger looks increasingly like Dos Equi
   s\' Most Interesting Man in the World, and his cryptic lyrics seem like
    an application for the title.\nBut the National rarely miss; when they
     aim for powerful or poetic, they get there. High Violet is the sound 
     of a band taking a mandate to be a meaningful rock band seriously, an
     d they play the part so fully that, to some, it may be off-putting. B
     ut these aren\'t mawkish, empty gestures; they\'re anxious, personal 
     songs projected onto wide screens.\xa0Even if you don\'t consider you
     rself an upwardly mobile stiff with minor social anxiety, the Nationa
     l make it sound grand, confusing, and relatable.\n''', 
     '2010', 'None', 
     8.7, 'The National')
add_album_to_sql(v)