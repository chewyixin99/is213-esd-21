from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

# Flask SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# initializing model
class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    wallet_id = db.Column(db.String(64), nullable=True)

    def __init__ (self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def json(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "wallet_id": self.wallet_id,
        }


@app.route("/user")
def get_all():
    users = User.query.all()
    if len(users):
        return jsonify(
            {
                "code":200,
                "data": {
                    "users": [
                        user.json() for user in users
                    ]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users"
        }
    )
    

@app.route("/user/<string:user_id>")
def find_by_user_id(user_id):
    
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )

    return jsonify(
        {
            "code": "404",
            "message": f"User with user id:{user_id} does not exist."
        }
    )

@app.route("/user/<string:email>", methods=["POST"])
def create_user(email):
    if (User.query.filter_by(email=email).first()):
        return jsonify(
            {
                "code": 400,
                "data": User.query.filter_by(email=email).first().json(),
                "message": f"User already exists.",
            }
        )
    data = request.get_json()
    user = User(email, **data)

    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "email": email,
                },
                "message": "An error occurred while creating user"
            }
        )
    return jsonify(
        {
            "code": 201,
            "data": user.json(),
            "message": "Created user."
        }
    )


    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)