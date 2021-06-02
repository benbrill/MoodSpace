import os
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy
import uuid
import json
import re
import numpy as np
from langdetect import detect

import lyricsgenius

import classification
import pandas as pd
from dotenv import load_dotenv

# import get_lyrics

load_dotenv();

genius = lyricsgenius.Genius()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')

@app.route('/')
def index():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private user-top-read',
                                                cache_handler=cache_handler, 
                                                show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    display_name = spotify.me()["display_name"]

    top_artists = spotify.current_user_top_artists(limit=5, offset=0, time_range='long_term')
    # TODO: if someone has very few top things, going up to 6 doesn't work.
    # in the template, we should probably have a for loop and make this variable length somehow
    artist_imgs = [top_artists['items'][i]['images'][0]['url'] for i in range(3)]
    top_artists = [top_artists['items'][i]['name'] for i in range(3)]


    top_tracks = spotify.current_user_top_tracks(limit=6, offset=0, time_range='long_term')
    top_track_names = [top_tracks['items'][i]['name'] for i in range(6)]
    top_track_artist_names = [top_tracks['items'][i]['artists'][0]['name'] for i in range(6)]
    top_track_imgs = [top_tracks['items'][i]['album']['images'][0]['url'] for i in range(6)]


    return render_template("Home.html", display_name=display_name, top_artists = top_artists, artist_imgs=artist_imgs, 
    top_track_names=top_track_names, top_track_imgs=top_track_imgs, top_track_artist_names=top_track_artist_names)
    
    
@app.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


@app.route('/playlists')
def playlists():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_playlists()


@app.route('/currently_playing')
def currently_playing():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    if not track is None:
        # my_classification = classification.main()
        song_title = track['item']['name']
        artist_name = track['item']['artists'][0]['name']


        genius_song = genius.search_song(song_title, artist_name)
        if genius_song is not None:
            return render_template("CurrentlyPlaying.html", track=track, lyrics=genius_song.lyrics, song_title=song_title, artist_name=artist_name)
        else:
            return render_template("CurrentlyPlaying.html", track=track, lyrics="Sorry, lyrics are not avaliable for this particular song", song_title=song_title, artist_name=artist_name)
    return "No track currently playing."


@app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()


@app.route('/choose_movie')
def choose_movie():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    with open('static/assets/movie_data.json') as f:
        data = json.load(f)
    return render_template("choose_movie.html", movies=list(data.keys()), chosen_movie=None)

@app.route('/choose_movie', methods=["POST"])
def choose_movie_post():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    chosen_movie = request.form['movie_scene']
    with open('static/assets/movie_data.json') as f:
        data = json.load(f)

    num_tracks = 10
    top_tracks = spotify.current_user_top_tracks(limit=num_tracks, offset=0, time_range='long_term')

    track_artist_name_pairs = {
        "track_name": [top_tracks['items'][i]['name'] for i in range(num_tracks)],
        "artists": [top_tracks['items'][i]['artists'][0]['name'] for i in range(num_tracks)],
        "id": [top_tracks['items'][i]['id'] for i in range(num_tracks)],
        }

    def get_lyrics(X):
        try:
            r = genius.search_song(X['track_name'], X['artists']).lyrics
        except:
            return None
        return r

    df = pd.DataFrame(track_artist_name_pairs)

    def stringProcessing(s):
        s = re.sub(r"\'", "", s)
        s = re.sub(r'\n', ' ', s)
        s = re.sub(r'\t', '', s)
        s = re.sub(r"\[[^[]*\]", '', s)
        s = re.sub(r'[^\w\s]', ' ', s)
        s = re.sub(r' +', ' ', s)
        s = s.strip()
        s = s.lower()
        return s

    df['lyrics'] = df.apply(get_lyrics, axis = 1)
    df = df[~df['lyrics'].isna()]
    df['lyrics'] = df['lyrics'].apply(stringProcessing)
    df['language'] = df['lyrics'].apply(detect)
    df = df[df['language'] == 'en']

    weights = classification.main(df)
    norms = np.linalg.norm(weights - np.array(data[chosen_movie]['weights']), axis = 1)
    ix = np.argsort(norms)
    sorted_df = df.iloc[ix]
    top_3_songs = sorted_df.iloc[0:3]['id']
    # df = pd.concat([df, pd.DataFrame(weights)], axis = 1)
    return render_template("choose_movie.html", movies=list(data.keys()), chosen_movie=data[chosen_movie], top_song_ids = top_3_songs)


'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
if __name__ == '__main__':
    app.run(threaded=True,debug=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", "8080").split(":")[-1])))