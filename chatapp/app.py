from flask import Flask
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import json


app = Flask(__name__)

# filename where to store stuff (sqlite is file-based)
db_name = 'chat.db'
# how do we connect to the database ?
# here we say it's by looking in a file named chat.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    done = db.Column(db.Boolean)

with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    return redirect('/front/notes')


@app.route('/api/notes', methods=['POST'])
def create_note():
    try:
        parameters = json.loads(request.data)
        title = parameters['title']
        content = parameters['content']
        done = parameters.get('done', False)
        print("received request to create note", title, content,done)
        # temporary
        new_note = Note(title=title, content=content,done=done)
        db.session.add(new_note)
        db.session.commit()
        return dict(message="Note created successfully"), 200
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422
    
@app.route('/api/list_notes', methods=['GET'])
def list_notes():
    notes = Note.query.all()
    return [dict(
            id=note.id, title=note.title, content=note.content, done=note.done)
        for note in notes]
    
@app.route('/front/notes')
def front_users():
    url = request.url_root + '/api/list_notes'
    req = request.get(url)
    if not (200 <= req.status_code < 300):
        # return render_template('errors.html', error='...')
        return dict(error=f"could not request notes list", url=url,
                    status=req.status_code, text=req.text)
    users = req.json()
    return render_template('notes.html.j2', users=users, version=VERSION)

if __name__ == '__main__':
    app.run()