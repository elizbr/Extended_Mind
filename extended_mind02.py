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



# Python code to remove duplicate elements >> https://www.geeksforgeeks.org/python-remove-duplicates-list/
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 



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
    REVIEW_DICT = em.open_cache(REVIEW_CACHE)

    #set variables
    name = request.form["name"]
    color = request.form["colors"]
    choice = request.form["choices"]
    print(2)

    


    #### CHECK SELECTIONS
    #user's COLOR choices 
    if color == 'desert':
        palette = "darkgoldenrod"#darkgoldenrod"
        plot_c = 'brown'
    elif color == 'valley':
        palette = 'greenyellow'  #'greenyellow' 
        plot_c = 'green'
    elif color == 'lake':
        palette = 'rgb(32, 80, 160)'
        plot_c = 'navy'
    else: 
        palette = 'white'
    print(3)
    

    ####### # process name 
    #check for existing data 
    if name in CACHE_DICT.keys():
        CACHE_DICT[name] = CACHE_DICT[name] + 1
        em.save_cache(CACHE_FILENAME, CACHE_DICT)
        print("Already In Cache, +1")
        query1 = f'''Select AlbumTitle FROM Albums Join Artists ON Albums.ArtistId = Artists.Id
        WHERE Artists.Name IS "{name}"'''
        try: 
            album_names = pull_content_sql(query1)
        except: 
            album_names = "No Album Information"
    else:
        album_names = [] 
        get_content = em.spotipy_call(name)
        CACHE_DICT[name] = 1
        em.save_cache(CACHE_FILENAME, CACHE_DICT)
        em.add_artist_to_sql(get_content.jjson())
        print("Adding to Cache, = 1")
        aaaa = get_content.list_of_albums()
        albums = Remove(aaaa)
        for x in albums:
            #print(x)
            if x == '':
                pass            
            else:
                try: 
                    print(x)
                    unique_key = f"{name}_{x}"
                    g = em.pitchfork.search(name, x)
                    try:
                        album_review = g.editorial()
                    except:
                        album_review = 'No Review'
                    album_names.append(x)
                    #print(album_review)
                    REVIEW_DICT[unique_key] = album_review
                    em.save_cache(REVIEW_CACHE, REVIEW_DICT)
                    #add sql 
                    try: 
                        after_g = em.album_scrape_p(name, x)
                        em.add_album_to_sql(after_g.jjson())
                    except: 
                        print("this is fucked.")
                except: 
                    unique_key = f"{name}_{x}"
                    REVIEW_DICT[unique_key] = 'No Review'
                    print('No Review Found, line 150 ish')
                    em.save_cache(REVIEW_CACHE, REVIEW_DICT)
                    try: 
                        #add sql 
                        #album_names.append(g.title)
                        em.add_album_to_sql(after_g.jjson())
                    except:
                        pass
    
    final_albums = Remove(album_names)


    query_albumratings = f'''
        SELECT AlbumScore FROM Albums JOIN Artists
        ON Albums.ArtistId = Artists.Id
        WHERE Artists.name = "{name}"
        ORDER BY Year ASC'''      

    query_albumtitles = f'''
        SELECT AlbumTitle FROM Albums JOIN Artists
        ON Albums.ArtistId = Artists.Id
        WHERE Artists.name = "{name}"
        ORDER BY Year ASC''' 

    query_albumyears = f'''
        SELECT Year FROM Albums JOIN Artists
        ON Albums.ArtistId = Artists.Id
        WHERE Artists.name = "{name}"
        ORDER BY Year ASC'''

    #user's INFO choices
    if choice == 'Album': 
        template = 'album.html'
        x_vals = []
        y_vals = []
        x_vals_needs = pull_content_sql(query_albumtitles)
        for x in x_vals_needs:
            x_vals.append(x[0]) #(query_albumtitles) 
        y_vals_needs = pull_content_sql(query_albumratings)
        for y in y_vals_needs:
            y_vals.append(y[0]) #(query_albumtitles) 
        if len(x_vals) < 1 :
            warning = 1
        else:
            warning = 0
        bars_data = go.Scatter(
            x=x_vals,
            y=y_vals,
            marker_color= plot_c)
        fig = go.Figure(data=bars_data)
        fig.update_yaxes(tickvals=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
        fig.update_layout(
            title=f"Pitchfork's Album Ratings for {name}",
            xaxis_title="Albums",
            yaxis_title="Album Rating (0-10)") 
        
        div = fig.to_html(full_html=False)

        return render_template(template, name = name, color = color, palette = palette, album_names = final_albums, plot_div=div, warning = warning)
    
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
        review_list = []
        for k,v in REVIEW_DICT.items():
            if k.split('_')[0] == name:
                title = k.split('_')[1]
                body = v.replace(r'/', '')
                album_entry = [title, body]
                if body != 'No Review':
                    review_list.append(album_entry)
        return render_template(template, name=name, color = color, palette = palette, review_list = review_list)
    
    elif choice == 'All':
        template = 'all.html'
        
        #album 
        x_vals = []
        y_vals = []
        x_vals_needs = pull_content_sql(query_albumtitles)
        for x in x_vals_needs:
            x_vals.append(x[0]) #(query_albumtitles) 
        y_vals_needs = pull_content_sql(query_albumratings)
        for y in y_vals_needs:
            y_vals.append(y[0]) #(query_albumtitles) 
        if len(x_vals) < 1 :
            warning = 1
        else:
            warning = 0
        bars_data = go.Scatter(
            x=x_vals,
            y=y_vals,
            marker_color= plot_c)
        fig = go.Figure(data=bars_data)
        fig.update_yaxes(tickvals=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]) 
        fig.update_layout(
            title=f"Pitchfork's Album Ratings for {name}",
            xaxis_title="Albums",
            yaxis_title="Album Rating (0-10)") 
        div = fig.to_html(full_html=False)
    
        #artist
        TTq = sql_query_builder('artist', "TT", name)
        Gq = sql_query_builder('artist', "G", name)
        SAq = sql_query_builder('artist', 'SA', name)
        SA = pull_content_sql(SAq)
        print(SA)
        print(TTq, Gq, SAq)

        #reviews
        review_list = []
        for k,v in REVIEW_DICT.items():
            if k.split('_')[0] == name:
                title = k.split('_')[1]
                body = v.replace(r'/', '')
                album_entry = [title, body]
                if body != 'No Review':
                    review_list.append(album_entry)

        return render_template(template, name=name, color = color, palette = palette, 
        review_list = review_list, SA = pull_content_sql(SAq), G = pull_content_sql(Gq), 
        TT = pull_content_sql(TTq), album_names = final_albums, plot_div=div, 
        warning = warning)
    
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


 