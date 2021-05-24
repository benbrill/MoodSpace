import os
from flask import Flask, session, request, redirect, render_template
from flask_session import Session
import spotipy
import uuid
import json

import lyricsgenius

# import Keras_Classification

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
    artist_1_img = top_artists['items'][0]['images'][0]['url']
    artist_2_img = top_artists['items'][1]['images'][0]['url']
    artist_3_img = top_artists['items'][2]['images'][0]['url']
    artist_4_img = top_artists['items'][3]['images'][0]['url']
    artist_5_img = top_artists['items'][4]['images'][0]['url']
    
    artist_1_name = top_artists['items'][0]['name']
    artist_2_name = top_artists['items'][1]['name']
    artist_3_name = top_artists['items'][2]['name']
    artist_4_name = top_artists['items'][3]['name']
    artist_5_name = top_artists['items'][4]['name']

    top_artists = [artist_1_name, artist_2_name, artist_3_name, artist_4_name, artist_5_name]
    artist_imgs = [artist_1_img, artist_2_img, artist_3_img, artist_4_img, artist_5_img] 

    top_tracks = spotify.current_user_top_tracks(limit=6, offset=0, time_range='long_term')
    top_tracks_1 = top_tracks['items'][0]['name']
    top_tracks_2 = top_tracks['items'][1]['name']
    top_tracks_3 = top_tracks['items'][2]['name']
    top_tracks_4 = top_tracks['items'][3]['name']
    top_tracks_5 = top_tracks['items'][4]['name']
    top_tracks_6 = top_tracks['items'][5]['name']

    artist_1_name = top_tracks['items'][0]['artists'][0]['name']
    artist_2_name = top_tracks['items'][1]['artists'][0]['name']
    artist_3_name = top_tracks['items'][2]['artists'][0]['name']
    artist_4_name = top_tracks['items'][3]['artists'][0]['name']
    artist_5_name = top_tracks['items'][4]['artists'][0]['name']
    artist_6_name = top_tracks['items'][5]['artists'][0]['name']

    top_track_1_img = top_tracks['items'][0]['album']['images'][0]['url']
    top_track_2_img = top_tracks['items'][1]['album']['images'][0]['url']
    top_track_3_img = top_tracks['items'][2]['album']['images'][0]['url']
    top_track_4_img = top_tracks['items'][3]['album']['images'][0]['url']
    top_track_5_img = top_tracks['items'][4]['album']['images'][0]['url']
    top_track_6_img = top_tracks['items'][5]['album']['images'][0]['url']

    top_track_names = [top_tracks_1, top_tracks_2, top_tracks_3, top_tracks_4, top_tracks_5, top_tracks_6]
    top_track_imgs = [top_track_1_img, top_track_2_img, top_track_3_img, top_track_4_img, top_track_5_img, top_track_6_img] 
    top_track_artist_names = [artist_1_name, artist_2_name, artist_3_name, artist_4_name, artist_5_name, artist_6_name]

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
        # classification = Keras_Classification.predict_mood(track['item']['id'])
        classification = None
        song_title = track['item']['name']
        artist_name = track['item']['artists'][0]['name']
        genius_song = genius.search_song(song_title, artist_name)
        lyrics=genius_song.lyrics
        if lyrics is not None:
            return render_template("CurrentlyPlaying.html", track=track, lyrics=genius_song.lyrics, classification=classification, song_title=song_title, artist_name=artist_name)
        else:
            return render_template("CurrentlyPlaying.html", track=track, lyrics="Sorry, lyrics are not avaliable for this particular song", classification=classification, song_title=song_title, artist_name=artist_name)
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
    return render_template("choose_movie.html", movies=list(data.keys()), chosen_movie=data[chosen_movie])


'''
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
'''
if __name__ == '__main__':
    app.run(threaded=True,debug=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", "8080").split(":")[-1])))