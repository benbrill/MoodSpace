import pandas as pd
import re

from langdetect import detect

from . import db, genius
from . import classification


def process_user_songs(top_tracks, my_user_id):

    track_artist_name_pairs = {
        "track_name": [top_tracks['items'][i]['name'] for i in range(len(top_tracks))],
        "artists": [top_tracks['items'][i]['artists'][0]['name'] for i in range(len(top_tracks))],
        "song_id": [top_tracks['items'][i]['id'] for i in range(len(top_tracks))],
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
    # df['lyrics'] = df['lyrics'].apply(stringProcessing)
    df['language'] = df['lyrics'].apply(detect)
    df = df[df['language'] == 'en']
    weights = classification.main(df)

    df['user_id'] = my_user_id
    df['weights'] = weights.tolist()
    # df = pd.concat([df, pd.DataFrame(weights)], axis = 1)
    df = df.drop(['lyrics'], axis=1)

    df.to_sql(name='songs', con=db.engine, index=False, if_exists='append')