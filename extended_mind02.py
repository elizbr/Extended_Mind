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