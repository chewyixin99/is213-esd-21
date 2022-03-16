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

    user_id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    wallet_id = db.Column(db.String(64), nullable=False)
    is_hawker = db.Column(db.Boolean, nullable=False)

    def __init__ (self, user_id, username, email, password, wallet_id, is_hawker):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.wallet_id = wallet_id
        self.is_hawker = is_hawker

    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "wallet_id": self.wallet_id,
            "is_hawker": self.is_hawker,
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

# Hawkers
@app.route("/hawker")
def get_hawkers():
    users = User.query.filter_by(is_hawker=True).all()
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
            "message": "There are no hawkers"
        }
    )

    
# @app.route("/customer/<string:customer_id>", methods=["POST"])
# def create_customer(customer_id):
#     pass

if __name__ == "__main__":
    app.run(port=5000, debug=True)