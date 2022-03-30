from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Flask SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost:3306/esd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# initializing model
class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    wallet_id = db.Column(db.String(64), nullable=True)

    def __init__ (self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
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
            "message": "User does not exist."
        }
    )

@app.route("/user/<string:email>", methods=["POST"])
def create_user(email):
    if (User.query.filter_by(email=email).first()):
        return jsonify(
            {
                "code": 400,
                "data": User.query.filter_by(email=email).first().json(),
                "message": "User already exists.",
            }
        )
    data = request.get_json()
    user = User(**data)

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
                "message": "An error occured while creating the book"
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
    app.run(port=5001, debug=True)