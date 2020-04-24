

#imports
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import os
import spotipy
import spotipy.util as util
import secrets
import requests
from bs4 import BeautifulSoup
import lxml
import pitchfork
import sqlite3
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data

#reference
# https://medium.com/@RareLoot/extracting-spotify-data-on-your-favourite-artist-via-python-d58bc92a4330
# https://github.com/michalczaplinski/pitchfork


os.environ["SPOTIPY_CLIENT_ID"] = secrets.spotify_id
os.environ["SPOTIPY_CLIENT_SECRET"] = secrets.spotify_secret

client_id = secrets.spotify_id
client_secret = secrets.spotify_secret
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API


#classes 
class Album:
    '''an album

    Instance Attributes 
    Title - str 
    Label - str 
    Editorial - str
    Cover - str 
    Year - str 
    Rating - float 
    Artist - str 
    '''
    def __init__(self, title = 'None', label = 'None', edit = 'None', cover = 'None', year = 0000, rating = 0.0, artist = 'None'):
        self.title = title 
        self.label = label 
        self.edit = edit 
        self.cover = cover 
        self.year = year
        self.rating = rating 
        self.artist = artist 

    def jjson(self):
        '''returns a list of content
        '''
        json_safe_t = [self.title, self.label, self.edit,self.cover, self.year, self.rating,self.artist]
        return  json_safe_t

class Artist:
    '''an artist

    Instance Attributes:
    '''
    def __init__(self, name = 'None', uri = 'None', genre = 'None', topsong1 = 'None', topsong2 = 'None', topsong3 = 'None', topsong4 = 'None', topsong5 = 'None', similartist1 = 'None', similartist2 = 'None', similartist3 = 'None', albumlist = 'None'):
        self.name = name 
        self.uri = uri
        self.genre = genre
        self.topsong1 = topsong1
        self.topsong2 = topsong2
        self.topsong3 = topsong3
        self.topsong4 = topsong4
        self.topsong5 = topsong5
        self.similarartist1 = similartist1
        self.similarartist2 = similartist2
        self.similarartist3 = similartist3
        self.albumlist = albumlist

    def jjson(self):
        '''returns a list of content
        '''
        json_safe_t = [self.name, self.uri, self.genre, self.topsong1, self.topsong2, self.topsong3, self.topsong4, self.topsong5, self.similarartist1, self.similarartist2, self.similarartist3, self.albumlist]
        return json_safe_t
    
    def list_of_albums(self):
        '''returns list of str albums'''
        albums = self.albumlist.split(',')
        return albums 
    

# set up cache
CACHE_FILENAME = 'cache.json'
CACHE_DICT = {}

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    If the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    dict
        The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

# Create the database & its tables
def create_db():
    conn = sqlite3.connect('albums.sqlite')
    cur = conn.cursor()
    #drop_bars_sql = 'DROP TABLE IF EXISTS "Bars"'
    #drop_countries_sql = 'DROP TABLE IF EXISTS "Countries"'

    target = '''PRAGMA foreign_keys = ON;'''

    create_artist_sql = '''

    CREATE TABLE IF NOT EXISTS "Artists" (
	"Id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Name"	TEXT,
	"SpotifyUri"	TEXT,
	"Genre"	TEXT,
	"TopSong1"	TEXT,
	"TopSong2"	TEXT,
	"TopSong3"	TEXT,
	"TopSong4"	TEXT,
	"TopSong5"	TEXT,
	"SimilarArtist1"	TEXT,
	"SimilarArtist2"	TEXT,
	"SimilarArtist3"	TEXT)'''

    create_album_sql = '''
            CREATE TABLE IF NOT EXISTS "Albums" (
	    "Id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	    "AlbumTitle"	TEXT,
	    "AlbumLabel"	TEXT,
	    "AlbumEditorial"	TEXT,
	    "AlbumCover"	TEXT,
        "Year"      NUMERIC,
	    "AlbumScore"	NUMERIC,
	    "ArtistId"	INTEGER NOT NULL,
        FOREIGN KEY (ArtistId)
        REFERENCES Artists (Id) 
        );'''

    #cur.execute(drop_bars_sql)
    #cur.execute(drop_countries_sql)

    cur.execute(target)
    cur.execute(create_artist_sql)
    cur.execute(create_album_sql)

    conn.commit()
    conn.close()


# spotify call

def spotipy_call(artist):
    '''makes api call to spotify and returns a bunch of info into an Artist'''
    result = sp.search(artist) #search query
    #print(result['tracks']['items'][0]['artists'])

    #Extract Artist's uri
    artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
    #Pull all of the artist's albums
    sp_albums = sp.artist_albums(artist_uri, album_type='album')
    sp_tracks = sp.artist_top_tracks(artist_uri, country = "US")
    sp_relatedartists = sp.artist_related_artists(artist_uri)
    #Store artist's albums' names' and uris in separate lists
    album_names = ''
    #album_uris = []
    list_albums = []
    for i in range(len(sp_albums['items'])):
        alnum = sp_albums['items'][i]['name']
        if alnum not in list_albums:
            list_albums.append(alnum)
            album_names = album_names + alnum + ', '
        #album_uris.append(sp_albums['items'][i]['uri'])

    track_names = [] 
    #track_uris = []
    for song in sp_tracks['tracks'][0:5]:
        track_names.append(song['name'])
        #track_uris.append(song['uri'])
    #print(track_names)

    genre = sp_relatedartists['artists'][0]['genres'][0]
    #print(genre)
    similar_artists = []
    #similar_a_uri = []
    for arty in sp_relatedartists['artists'][0:3]:
        similar_artists.append(arty['name'])
        #similar_a_uri.append(artist['uri'])
    #print(similar_artists)
    #print(genre)
    #print(album_names)
    return Artist(name = artist, uri=artist_uri, genre = genre, topsong1= track_names[0], topsong2=track_names[1], topsong3=track_names[2], topsong4=track_names[3], topsong5=track_names[4], similartist1 = similar_artists[0], similartist2=similar_artists[1], similartist3=similar_artists[2], albumlist= album_names)

#scrape spotify with cache
def artist_scrape_cache(art_obj):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    endpoint_url: string
        API endpoint URL 
    result_obj: dict
        Dictionary of returned info
    
    Returns
    -------
    dict
        query results in JSON / dict 
    '''
    if art_obj in CACHE_DICT.keys():
        print("Using Cache")
        y = CACHE_DICT[art_obj]
        #print(y)
        return Artist(name=y[0], uri = y[1], genre = y[2], topsong1= y[3], topsong2=y[4], topsong3 =y[5], topsong4=y[6], topsong5=y[7], similartist1=y[8], similartist2=y[10], similartist3=y[11], albumlist=y[12])
    else:
        print("Fetching")
        content = spotipy_call(art_obj)
        CACHE_DICT[art_obj] = content.jjson()
        #print(content.jjson())
        save_cache(CACHE_DICT)
        #add_artist_to_sql(content.jjson())
        add_artist_to_sql(content.jjson())
        return content


#scrape pitchfork for album reviews 

#2. Extract data records from the CSV and Web API. 

#scrape pitchfork with cache 
def album_scrape_p(artist, album):
    '''takes artist and album and creates dict for each 
    album available on pitchfork 
    Parameters:
    _artist <str> - Artist Name
    _album <album name> - Artist's specificed album 
    Returns:
    _album_content <Album> - contains all info 
    necessary for db add 
    '''
    p = pitchfork.search(artist, album) # the title is autocompleted
    x = p.year()
    if len(x) != 4:
        try: 
            y = x.split('-').strip()
            x = y[0]
            x = int(x)
        except:
            x = 0000
    
    g = p.editorial()
    mf = g.replace('/','')

        
    title = p.album() # the full album title
    label = p.label()
    edit = mf
    rating = p.score()
    artist = p.artist()
    year = int(x)
    try: 
        cover = p.cover()
    except:
        cover = 'None'
    return Album(title= title, label = label, edit= edit, cover = cover, year = year, rating = rating, artist = artist)


def result_obj(artist, album):
    obj = f"{artist}_{album}"
    return obj 


def album_scrape_cache(result_obj, artist, album):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    endpoint_url: string
        API endpoint URL 
    result_obj: dict
        Dictionary of returned info
    
    Returns
    -------
    dict
        query results in JSON / dict 
    '''
    if result_obj in CACHE_DICT.keys():
        print("Using Cache")
        y = CACHE_DICT[result_obj]
        return Album(title=y[0], label=y[1], edit = y[2], cover = y[3], year = y[4], rating = y[5], artist = y[6])
    else:
        print("Fetching")
        content = album_scrape_p(artist, album)
        CACHE_DICT[result_obj] = content.jjson()
        #print(content.title)
        save_cache(CACHE_DICT)
        add_album_to_sql(content.jjson())
        return CACHE_DICT[result_obj]

#3. Insert each extracted record into the DB, making sure that the 
#relationships between Bars and Countries are correctly represented.

#assign album info to album.sql
def add_album_to_sql(cont):
    try:
        conn = sqlite3.connect('albums.sqlite')
        cur = conn.cursor()
        print("Successfully Connected to SQLite")


        insert_query = f'''INSERT INTO Albums
        (AlbumTitle, AlbumLabel, AlbumCover, Year, AlbumScore, ArtistId) 
        VALUES ("{cont[0]}", "{cont[1]}", "{cont[3]}", {cont[4]}, {cont[5]}, (SELECT Id from Artists WHERE Name = "{cont[6]}"));
        '''
        print(insert_query)
        cur.execute(insert_query)
        conn.commit()
        conn.close()

    except:
        print("Failed to insert data into sqlite table")
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")


#assign artist info to artist.sql
def add_artist_to_sql(cont):
    insert_query = f'''INSERT INTO Artists
        (Name, SpotifyUri, Genre, TopSong1, TopSong2, TopSong3, TopSong4, 
        TopSong5, SimilarArtist1, SimilarArtist2, SimilarArtist3) 
        VALUES ("{cont[0]}", "{cont[1]}", "{cont[2]}", "{cont[3]}", 
        "{cont[4]}", "{cont[5]}", "{cont[6]}", "{cont[7]}", "{cont[8]}", 
        "{cont[9]}", "{cont[10]}")'''

    print(insert_query)

    try:
        conn = sqlite3.connect('albums.sqlite')
        cur = conn.cursor()
        print("Successfully Connected to SQLite")

        cur.execute(insert_query)
        conn.commit()
        conn.close()

    except:
        print("Failed to insert data into sqlite table")
    finally:
        if (conn):
            conn.close()
            print("The SQLite connection is closed")
    


# User input for artist 
#flask interfact for user 
"""
from flask import Flask, render_template, request
import sqlite3
import plotly.graph_objects as go

app = Flask(__name__)
"""



################

if __name__ == "__main__":
    CACHE_DICT = open_cache()
    create_db()
    switch = 'one'
    while switch == 'one':
        artist = input(f"What is your artist pick?")
        try: 
            people = artist_scrape_cache(artist)
            switch = 'two'
        except:
            print("Try again")

    all_albums = people.list_of_albums()
    for a in all_albums:
        try: 
            print('one')
            obj = result_obj(artist, a)
            print('two')
            if obj in CACHE_DICT.keys():
                print('already json-ed')
                pass
            else:
                print('three')
                album_scrape_cache(obj, artist, a)
        except:
            print('passing at except')
            pass
    #print(len(albums_folder))
 
