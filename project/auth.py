from flask import Blueprint, redirect, url_for, request, flash, session
import uuid
import os

import spotipy
from dotenv import load_dotenv
load_dotenv();

# from . import db, session_cache_path
from . import session_cache_path
# from .models import Songs
from .ml import process_user_songs

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())

    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-public user-library-read  user-top-read',
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
    # auth_manager.get_access_token(request.args.get("code"))
    # spotify = spotipy.Spotify(auth_manager=auth_manager)
    # num_tracks = 10
    # top_tracks = spotify.current_user_top_tracks(limit=num_tracks, offset=0, time_range='long_term')
    # process_user_songs(top_tracks, spotify.me()['id'])
    return redirect(url_for('main.profile'))
    
@auth.route('/sign_out')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')