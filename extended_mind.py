

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
    def __init__(self, name = 'None', genre = 'None', bio = 'None', topalbum = 'None', toptracks = 'None', albumlist = 'None'):
        self.name = name 
        self.genre = genre
        self.bio = bio 
        self.topalbum = topalbum
        self.toptracks = toptracks
        self.albumlist = albumlist

    def jjson(self):
        '''returns a list of content
        '''
        json_safe_t = [self.name, self.genre, self.bio, self.topalbum, self.toptracks, self.albumlist]
        return json_safe_t
    

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

    create_album_sql = '''
        CREATE TABLE IF NOT EXISTS "Albums" (
	    "Id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	    "AlbumTitle"	TEXT,
	    "AlbumLabel"	TEXT,
	    "AlbumEditorial"	TEXT,
	    "AlbumCover"	TEXT,
        "Year"      NUMERIC,
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


# spotify call



name = "radiohead" #chosen artist
result = sp.search(name) #search query
#print(result['tracks']['items'][0]['artists'])


#Extract Artist's uri
artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
#Pull all of the artist's albums
sp_albums = sp.artist_albums(artist_uri, album_type='album')
sp_tracks = sp.artist_top_tracks(artist_uri, country = "US")
sp_relatedartists = sp.artist_related_artists(artist_uri)
#Store artist's albums' names' and uris in separate lists
album_names = []
album_uris = []
for i in range(len(sp_albums['items'])):
    album_names.append(sp_albums['items'][i]['name'])
    album_uris.append(sp_albums['items'][i]['uri'])

track_names = [] 
track_uris = []
for song in sp_tracks['tracks']:
    track_names.append(song['name'])
    track_uris.append(song['uri'])
#print(track_uris)

genres = sp_relatedartists['artists'][0]['genres']
print(genres)
similar_artists = []
similar_a_uri = []
for artist in sp_relatedartists['artists']:
    similar_artists.append(artist['name'])
    similar_a_uri.append(artist['uri'])





#scrape pitchfork for album reviews 


#scrape spotify with cache


#scrape pitchfork with cache 


#2. Extract data records from the CSV and Web API. 
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
def add_album_to_sql(cont):
    try:
        conn = sqlite3.connect('albums.sqlite')
        cur = conn.cursor()
        print("Successfully Connected to SQLite")

        insert_query = f'''INSERT INTO Albums
        (AlbumTitle, AlbumLabel, AlbumCover, Year, AlbumScore, ArtistTitle) 
        VALUES ("{cont[0]}", "{cont[1]}", "{cont[3]}", {cont[4]}, {cont[5]}, "{cont[6]}")'''

        cur.execute(insert_query)
        conn.commit()
        conn.close()

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
"""
from flask import Flask, render_template, request
import sqlite3
import plotly.graph_objects as go

app = Flask(__name__)
"""

"""
album = 'Sunbather'
artist = 'Deafheaven'
cont = album_scrape_p(artist, album).jjson()
#print(x.edit)
print(f'''INSERT INTO Albums
        (AlbumTitle, AlbumLabel, AlbumCover, Year, AlbumScore, ArtistTitle) 
        VALUES ("{cont[0]}", "{cont[1]}", "{cont[3]}", "{cont[4]}", "{cont[5]}", "{cont[6]}")''')
"""


import spotipy
import spotipy.util as util
scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for", username)

"""def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None"""

name = "radiohead" #chosen artist
result = sp.search(name) #search query
print(result['tracks']['items'][0]['artists'])
#x = get_artist("Radiohead")
#print(x)

################
"""
if __name__ == "__main__":
    CACHE_DICT = open_cache()
    create_db()
    artist = input(f"What is your artist pick?")
    album = input("album: ")

    obj = result_obj(artist, album)
    v = album_scrape_cache(obj, artist, album)
        
"""
