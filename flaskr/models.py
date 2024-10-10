from flaskr.db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_song_user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('songs', lazy=True))


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_playlist_user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('playlists', lazy=True))


class PlaylistSong(db.Model):
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id', name='fk_playlistsong_playlist_id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id', name='fk_playlistsong_song_id'), primary_key=True)
    playlist = db.relationship('Playlist', backref=db.backref('playlist_songs', lazy=True))
    song = db.relationship('Song', backref=db.backref('playlist_songs', lazy=True))
