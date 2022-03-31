from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Flask SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost:3306/esd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# initializing model
class Hawker(db.Model):
    __tablename__ = "hawker"

    hawker_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    wallet_id = db.Column(db.Integer, nullable=True)
    cuisine = db.Column(db.String(64), nullable=True)
    halal = db.Column(db.Boolean(), nullable=False)
    has_vegetarian_option = db.Column(db.Boolean(), nullable=False)

    def __init__ (self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def json(self):
        return {
            "hawker_id": self.hawker_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "wallet_id": self.wallet_id,
            "cuisine": self.cuisine,
            "halal": self.halal,
            "has_vegetarian_option": self.has_vegetarian_option,
        }

# Get all hawkers
@app.route("/hawker")
def get_all():
    hawkers = Hawker.query.all()
    if len(hawkers):
        return jsonify(
            {
                "code":200,
                "data": {
                    "hawkers": [
                        hawker.json() for hawker in hawkers
                    ]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no hawkers."
        }
    )
    
# Get hawker by hawker id
@app.route("/hawker/<string:hawker_id>")
def find_by_hawker_id(hawker_id):
    
    hawker = Hawker.query.filter_by(hawker_id=hawker_id).first()
    if hawker:
        return jsonify(
            {
                "code": 200,
                "data": hawker.json()
            }
        )
    return jsonify(
        {
            "code": "404",
            "message": "hawker does not exist."
        }
    )

# Create hawker
@app.route("/hawker/<string:email>", methods=["POST"])
def create_hawker(email):
    hawker = Hawker.query.filter_by(email=email).first()
    if (hawker):
        return jsonify(
            {
                "code": 400,
                "data": hawker.json(),
                "message": "Hawker already exists.",
            }
        )
    
    # 
    data = request.get_json()
    hawker = Hawker(data['username'], email, data['password'])
    for key in data.keys():
        if not (key in ['username', 'email', 'password']):
            setattr(hawker, key, data[key])

    try:
        db.session.add(hawker)
        db.session.commit()

    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "email": email
                },
                "message": "An error occurred while creating hawker."
            }
        )
    return jsonify(
        {
            "code": 201,
            "data": hawker.json(),
            "message": "Created hawker."
        }
    )

# Update hawker
@app.route("/hawker/<int:hawker_id>", methods=['PUT'])
def update_hawker(hawker_id):
    hawker = Hawker.query.filter_by(hawker_id=hawker_id).first()
    
    if not (hawker):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "hawker_id": hawker_id
                },
                "message": f"Requested hawker (with hawker id {hawker_id}) does not exist."
            }
        ), 404

    data = request.get_json()

    try:
        for key in data.keys():            
            setattr(hawker, key, data[key])
        db.session.commit()
        
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "hawker_id": hawker_id
                },
                "message": "An error occurred while updating the hawker."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": hawker.json(),
            "message": "Successfully updated hawker."
        }
    ), 201


if __name__ == "__main__":
    app.run(port=5002, debug=True)