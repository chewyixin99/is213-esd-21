from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Flask SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/esd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# initializing model
class Hawker(db.Model):
    __tablename__ = "hawker"

    hawker_id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    wallet_id = db.Column(db.String(64), nullable=False)

    def __init__ (self, hawker_id, username, email, password, wallet_id):
        self.hawker_id = hawker_id
        self.username = username
        self.email = email
        self.password = password
        self.wallet_id = wallet_id

    def json(self):
        return {
            "hawker_id": self.hawker_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "wallet_id": self.wallet_id,
        }


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
            "message": "There are no hawkers"
        }
    )
    

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
            "message": "Hawker does not exist."
        }
    )

# @app.route("/hawker/<string:hawker_id>", methods=["POST"])
# def create_hawker(hawker_id):
#     pass

if __name__ == "__main__":
    app.run(port=5000, debug=True)