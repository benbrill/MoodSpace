from flask import request, redirect, render_template, Blueprint
import json
import pandas as pd
import numpy as np
import string
import random

# from . import db, genius, session_cache_path
from . import genius, session_cache_path
# from .models import Songs
from dotenv import load_dotenv
from .ml import process_user_songs

load_dotenv();

import spotipy

main = Blueprint('main', __name__)


@main.route('/profile')
def profile():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

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
    


@main.route('/playlists')
def playlists():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_playlists()


@main.route('/currently_playing')
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


@main.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()


@main.route('/choose_movie')
def choose_movie():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    with open('project/static/assets/movie_data.json') as f:
        data = json.load(f)
    return render_template("choose_movie.html", movies=list(data.keys()), chosen_movie=None)

@main.route('/choose_movie', methods=["POST"])
def choose_movie_post():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    display_name = spotify.me()["display_name"]

    # playlist_name = f"{display_name}'s Mood Playlist" 
    
    # # playlists = spotipy.Spotify.user_playlists(display_name)
    # playlists = spotify.current_user_playlists()
    # for playlist in playlists['items']:  # iterate through playlists I follow
    #     if playlist['name'] == playlist_name:  # filter for newly created playlist
    #         playlist_id = playlist['id']

    # retrieve our metadata around the movie the user chose
    chosen_movie = request.form['movie_scene']
    with open('project/static/assets/movie_data.json') as f:
        data = json.load(f)

    # retrieve user's songs and associated weights from db
    # df = pd.read_sql(db.session.query(Songs).filter(Songs.user_id == spotify.me()['id']).statement, db.engine)
    num_tracks = 50
    offset = random.choice(string.digits)
    top_tracks = spotify.current_user_top_tracks(limit=num_tracks, offset=offset, time_range='long_term')
    df = process_user_songs(top_tracks, spotify.me()['id'])
    
    weights = np.array(df['weights'].values.tolist())
    
    # calculate songs closest in weight to movie weights
    norms = np.linalg.norm(weights - np.array(data[chosen_movie]['weights']), axis = 1)
    ix = np.argsort(norms)
    sorted_df = df.iloc[ix]
    top_3_songs = sorted_df.iloc[0:3]['song_id']

    #creates playlist with top songs
    # spotify.user_playlist_create(user=spotify.me()["id"], name=playlist_name)
    # spotify.user_playlist_add_tracks(user=spotify.me()["id"], playlist_id=playlist_id, tracks=top_3_songs)

    #return render_template("choose_movie.html", movies=list(data.keys()), chosen_movie=data[chosen_movie], top_song_ids = top_3_songs, playlist_id=playlist_id)
    return render_template("choose_movie.html", movies=list(data.keys()), chosen_movie=data[chosen_movie], top_song_ids = top_3_songs,)

    