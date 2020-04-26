

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
import plotly
import colorlover as cl

from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    os.environ["SPOTIPY_CLIENT_ID"] = secrets.spotify_id
    os.environ["SPOTIPY_CLIENT_SECRET"] = secrets.spotify_secret
    return render_template('index.html') # just the static HTML

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    em.create_db()
    em.open_cache(em.CACHE_FILENAME)
    artist = request.form["name"]
    color = request.form["colors"]

    try:
        people = em.artist_scrape_cache(artist)
        #print("here")
        #print(people.albumlist)
        failed = 0
        try: 
            all_albums = people.list_of_albums()
            #print(all_albums)
        except:
            all_albums = 0
    except:
        all_albums = 0

    album_json_contents = [] 
        
    if all_albums != 0:
        for a in all_albums:
            try: 
                #print(f" Album: {a}")
                #print(a)
                obj = em.result_obj(artist, a)
                #print("here")
                #print('Searching Cache')
                if obj in em.CACHE_DICT.keys():
                    #print(f"Found {a}.")
                    album = em.Album(em.CACHE_DICT[obj])
                    print("here")
                    album_json_contents.append(album)
                    print("here")
                    failed = 0 
                else:
                    #print(f"Creating {a}.")
                    album = em.album_scrape_cache(obj, artist, a)
                    print("kkkkhere")
                    album_json_contents.append(album)
                    print("kkkkhere")
                    failed = 0 
            except:
                failed = 1 
                print("failed here")
                #print(f'Trouble while looking for {a}.')
    elif all_albums == 0:
        failed = 1 
        print("total fail")
    
    if failed == 0:
        ratings = []
        album_titles = [] 
        reviews = [] 
        years = []

        for album_l in album_json_contents:
            try: 
                years.append(album_l.year)
                album_titles.append(album_l.title)
                ratings.append(album_l.rating)
                reviews.append(album_l[2])
            except:
                years.append("No Year")
                album_titles.append("No Title")
                ratings.append("No Rating")
                reviews.append("No Review")
            


        results = em.get_albums_by_rating(artist)
        if len(results) != 0:
            make_graph = 1
        elif len(results) == 0:
            make_graph = 0


        x_vals = album_titles
        y_vals = ratings
        bars_data = go.Bar(
                x=x_vals,
                y=y_vals
                )
        fig = go.Figure(data=bars_data)
        div = fig.to_html(full_html=False)


        tracks = em.get_artist_top_tracks(artist)
        top_tracks = tracks[0][4:8]
        genre = tracks[0][3]
        similar_artists = tracks[0][9:11]
        

        return render_template('response.html', 
            name=artist,
            list_albums = all_albums,
            color=color, 
            contents = album_json_contents, 
            years = years,
            genre = genre,
            album_titles = album_titles,
            similar_artists = similar_artists,
            ratings = ratings, 
            reviews = reviews, 
            results = results,
            make_graph = make_graph,
            plot_div=div) 

    elif failed == 1: 
        return render_template('invalid_response.html', 
            name=artist,
            color=color) 



if __name__ == "__main__":
    app.run(debug=True)


