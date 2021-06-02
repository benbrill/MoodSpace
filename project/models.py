from . import db

# Building user model
class Songs(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20))
    track_name = db.Column(db.String(200))
    artists = db.Column(db.String(200))
    song_id = db.Column(db.String(200))
    language = db.Column(db.String(20))

    weights = db.Column(db.Float)
    

    def __init__(self, user_id, track_name, artists, song_id, language, weights):
        self.user_id = user_id
        self.track_name = track_name
        self.artists = artists
        self.song_id = song_id
        self.language = language
        self.weights = weights