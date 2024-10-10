from flask import Blueprint, request, url_for, redirect, render_template
from flaskr.models import db, Song

from wtforms import Form, StringField, validators

# Define the blueprint
bp = Blueprint('song', __name__)  # Added url_prefix

# Song form definition
class SongForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=25)])
    artist = StringField('Artist', [validators.Length(min=4, max=25)])

# Index route to list songs
@bp.route('/', methods=['GET'])
def index():
    songs = Song.query.all()
    return render_template('song/index.html', songs=songs)

# Route to add new songs
@bp.route('/addsong', methods=['GET', 'POST'])
def addSongs():
    form = SongForm(request.form)
    if request.method == "POST" and form.validate():
        title = request.form['title']
        artist = request.form['artist']
        new_song = Song(title=title, artist=artist)
        db.session.add(new_song)
        db.session.commit()
        return redirect(url_for('songs.index'))  # Fixed redirect to the correct endpoint

    return render_template('song/add.html', form=form)  # Pass the form to the template
