from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'ppostgresql+psycopg2://japiosmuawoeif:5fb7865a30ccd9848356a018582cee7186472ddafe35b23aa61cbe6fa969a357@ec2-54-86-106-48.compute-1.amazonaws.com:5432/d4e37uperu0jod'
db = SQLAlchemy(app)
from flask_sqlalchemy import SQLAlchemy

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    pet_data = request.get_json()
    if request.method == 'POST':
        email = pet_data['name']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()