

#imports
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import spotipy
import spotipy.util as util
import secrets

#enviro exports
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


#scrape pitchfork with cache 
import requests
from bs4 import BeautifulSoup

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

#print(format_album_query('High Violet'))
#print(format_album_query('Sunbather'))

## Make the soup
def make_soup(sunbather):  
    url = f'https://pitchfork.com/search/?query={sunbather}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ## Get the searching-div
    searching_div = soup.find(class_ ="review__link")
    print(searching_div) # sanity check, delete after it checks out

    c_link = soup.find('href', class_='section', recursive=False)


    ## Loop through the child divs, print header
    child_divs = nav_div.find_all('div', class_='section', recursive=False)
    for c_div in child_divs:
        c_header = c_div.find('h2')
        print(c_header.text)

    return c_header ## sanity check, delete after it checks out

#x = make_soup('sunbather')
#print(x) 
## Get the searching-div

## Loop through the child divs, print header

## Loop through the grandchild divs, print header



#assign album info to album.sql 


#assign artist info to artist.sql


# User input for artist 


#flask interfact for user 

'''
birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
        
'''