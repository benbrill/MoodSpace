import pandas as pd
import re

from langdetect import detect

from . import db, genius
from . import classification
from .models import Songs


def process_user_songs(top_tracks, my_user_id):
    """
    inputs the response from the Spotify API of a user's top tracks. Then, gets the lyrics for each song
    using the Genius API and prepares them for vectorization. Our model is then run on these lyrics to 
    extract the predicted Spotify metrics, and these numbers are appended to our PostgreSQL server.
    """

    num_tracks = len(top_tracks['items'])
    
    # create dict of top songs for data frame creation
    track_artist_name_pairs = {
        "track_name": [top_tracks['items'][i]['name'] for i in range(num_tracks)],
        "artists": [top_tracks['items'][i]['artists'][0]['name'] for i in range(num_tracks)],
        "song_id": [top_tracks['items'][i]['id'] for i in range(num_tracks)],
        }

    def get_lyrics(X):
        """
        takes in a Artist name and track name from a data frame and returns lyrics. If an error is 
        encountered, automatically returns none
        """
        try:
            r = genius.search_song(X['track_name'], X['artists']).lyrics
        except:
            return None
        return r

    df = pd.DataFrame(track_artist_name_pairs)

    def stringProcessing(s):
        """
        preprocess lyrics to remove unneccesary insertions and spaces
        """
        s = re.sub(r"\'", "", s)
        s = re.sub(r'\n', ' ', s)
        s = re.sub(r'\t', '', s)
        s = re.sub(r"\[[^[]*\]", '', s)
        s = re.sub(r'[^\w\s]', ' ', s)
        s = re.sub(r' +', ' ', s)
        s = s.strip()
        s = s.lower()
        return s

    df['lyrics'] = df.apply(get_lyrics, axis = 1) # get lyrics for each song
    df = df[~df['lyrics'].isna()] # remove songs with no lyrics
    df['lyrics'] = df['lyrics'].apply(stringProcessing) # preprocess lyrics
    df['language'] = df['lyrics'].apply(detect) # detect language of lyrics
    df = df[df['language'] == 'en'] # use only lyrics that are in english
    weights = classification.main(df) # get weights for each lyric

    df['user_id'] = my_user_id
    df['weights'] = weights.tolist()
    df = df.drop(['lyrics'], axis=1)

    Songs.query.filter_by(user_id=my_user_id).delete()
    db.session.commit()


    df.to_sql(name='songs', con=db.engine, index=False, if_exists='append')
