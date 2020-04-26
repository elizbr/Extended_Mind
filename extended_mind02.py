#imports
import plotly.graph_objects as go
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
import extended_mind as em
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import extended_mind as em 
from flask import Flask, render_template, request
from extended_mind import Artist, Album
app = Flask(__name__)
CACHE_FILENAME = 'cache.json'
CACHE_DICT = {}
REVIEW_CACHE = 'reviews.json'
REVIEW_DICT = {}

#back up fxns
def get_artist_info_from_sql(artist):
    '''return stored artist info'''
    conn = sqlite3.connect('albums.sqlite')
    cur = conn.cursor()
    q = f'''
        SELECT *
        FROM Artists
        WHERE name IS "{artist}"
        '''
    cur.execute(q)



def sql_query_builder(t, content, artist):
    '''t - artist or album 
    content - artist name or album name'''
    if t == 'artist':
        if content == 'SA':
            q = f''' SELECT SimilarArtist1, 
            SimilarArtist2, SimilarArtist3
            FROM Artists WHERE name = "{artist}" '''
        if content == 'TT':
            q = f'''SELECT TopSong1, TopSong2, 
            TopSong3, TopSong4, TopSong5
            FROM Artists
            WHERE name = "{artist}" '''
        if content == 'G':
            q = f'''SELECT Genre
            FROM Artists
            WHERE name = "{artist}" '''
        if content == 'URI':
            q = f'''SELECT SpotifyUri
            FROM Artists
            WHERE name = "{artist}" '''
    if t == 'album':
        pass
    return q


def pull_content_sql(q):
    '''return stored artist info'''
    conn = sqlite3.connect('albums.sqlite')
    cur = conn.cursor()
    cur.execute(q)
    return cur.fetchall()





@app.route('/')
def index():
    CACHE_DICT = em.open_cache(CACHE_FILENAME)
    try: 
        highest_score = max(CACHE_DICT.items(), key=lambda x : x[1])
        high = highest_score[0]
    except:
        high = 'Deafheaven'
    #print(high)
    return render_template('index.html', high = high) # just the static HTML


@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    #set up 
    print(1)
    em.create_db()
    CACHE_DICT = em.open_cache(CACHE_FILENAME)

    #set variables
    name = request.form["name"]
    color = request.form["colors"]
    choice = request.form["choices"]
    print(2)

    #### CHECK SELECTIONS
    #user's COLOR choices 
    if color == 'desert':
        palette = 0 #desert_colors 
    elif color == 'valley':
        palette = 1 #lake_colors 
    elif color == 'lake':
        palette = 2 #valley_colors 
    else: 
        palette = 0
    print(3)
    

    ####### # process name 
    #check for existing data 
    if name in CACHE_DICT.keys():
        CACHE_DICT[name] = CACHE_DICT[name] + 1
        em.save_cache(CACHE_FILENAME, CACHE_DICT)
        print("Already In Cache, +1")
    else:
        get_content = em.spotipy_call(name)
        CACHE_DICT[name] = 1
        em.save_cache(CACHE_FILENAME, CACHE_DICT)
        em.add_artist_to_sql(get_content.jjson())
        print("Adding to Cache, = 1")
      

    #user's INFO choices
    if choice == 'Album':
        template = 'album.html'
    elif choice == 'Artist':
        template = 'artist.html'
        TTq = sql_query_builder('artist', "TT", name)
        Gq = sql_query_builder('artist', "G", name)
        SAq = sql_query_builder('artist', 'SA', name)
        SA = pull_content_sql(SAq)
        print(SA)
        print(TTq, Gq, SAq)
        return render_template(template, name = name, color = color, palette = palette, SA = pull_content_sql(SAq), G = pull_content_sql(Gq), TT = pull_content_sql(TTq))
    elif choice == 'Review':
        template = 'review.html'
    elif choice == 'All':
        template = 'all.html'
    else:
        template = 'invalid_response.html'
    print(4)


if __name__ == "__main__":
    app.run(debug=True)
    





    # ####GET INFO  

    #artist variable 
    #check for cache version
    #populate SQLite
    #populate cache 

    #albums --- 
    #check for cache version
    #populate SQLite 
    #populate cache 

    # ##### USE INFO 
    #graph years, ratings & names of albums 
    #print an album review 
    #Print list of albums 
    #print genre 
    #print print similar artists 