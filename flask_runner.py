

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
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import extended_mind as em 

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') # just the static HTML

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    artist = request.form["name"]
    secret = request.form["secret"]
    color = request.form["colors"]

    try:
        people = em.artist_scrape_cache(artist)
        failed = 0
        try: 
            all_albums = people.list_of_albums()
        except:
            all_albums = 0
    except:
        all_albums = 0

    album_json_contents = [] 
        
    if all_albums != 0:
        for a in all_albums:
            try: 
                #print(f" Album: {a}")
                obj = em.result_obj(artist, a)
                #print('Searching Cache')
                if obj in em.CACHE_DICT.keys():
                    #print(f"Found {a}.")
                    album = em.Album(CACHE_DICT[obj])
                    album_json_contents.append(album)
                    failed = 0 
                else:
                    #print(f"Creating {a}.")
                    album = em.album_scrape_cache(obj, artist, a)
                    album_json_contents.append(album)
                    failed = 0 
            except:
                failed = 1 
                #print(f'Trouble while looking for {a}.')
    elif all_albums == 0:
        failed = 1 
    
    if failed == 0:

        ratings = []
        album_titles = [] 
        reviews = [] 
        years = []

        for album_l in album_json_contents:
            try: 
                years.append(album_l[-3])
                album_titles.append(album_l[1])
                ratings.append(album_l[-2])
                reviews.append(album_l[2])
            except:
                years.append("No Year")
                album_titles.append("No Title")
                ratings.append("No Rating")
                reviews.append("No Review")

        results = em.get_albums_by_rating('Deafheaven')
        if len(results) != 0:
            make_graph = 1
        elif len(results) == 0:
            make_graph = 0

        return render_template('response.html', 
            name=artist, 
            secret=secret,
            list_albums = all_albums,
            color=color, 
            contents = album_json_contents, 
            years = years,
            album_titles = album_titles,
            ratings = ratings, 
            reviews = reviews, 
            results = results,
            make_graph = make_graph) 
    elif failed == 1: 
        return render_template('invalid_response.html', 
            name=artist, 
            secret=secret,
            color=color) 


@app.route('/results')
def res():
    conn = sqlite3.connect('albums.sqlite')
    cur = conn.cursor()
    q = '''
        SELECT AlbumTitle, Rating
        FROM Albums
        ORDER BY Year DESC
        LIMIT 5
    '''
    cur.execute(q)

    bars = cur.fetchall()

    return render_template('results.html', bars=bars)



if __name__ == "__main__":
    app.run(debug=True)


