from flask import Flask, render_template, request, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://japiosmuawoeif:5fb7865a30ccd9848356a018582cee7186472ddafe35b23aa61cbe6fa969a357@ec2-54-86-106-48.compute-1.amazonaws.com:5432/d4e37uperu0jod'
db = SQLAlchemy(app)
from flask_sqlalchemy import SQLAlchemy
CORS(app)

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


@cross_origin()
@app.route('/prereg', methods=['POST'])
def prereg():
    pet_data = request.get_json()
    if request.method == 'POST':
        email = pet_data['email']
        reg = User(email=email)
        db.session.add(reg)
        db.session.commit()
        print('hello')
        return render_template('success.html')
        # Check that email does not already exist (not a great query, but works)

    return render_template('index.html')
@cross_origin()
@app.route('/getpets', methods = ['GET'])
def getpets():
     all_pets = []
     pets = User.query.all()
     for pet in pets:
          results = {
                    "pet_id":pet.id,
                    "email":pet.email,
        }
          all_pets.append(results)

     return jsonify(
            {
                "success": True,
                "pets": all_pets,
                "total_pets": len(pets),
            }
        )
if __name__ == '__main__':
    app.debug = True
    app.run(port=2000, debug=True)