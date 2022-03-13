from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Flask SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/esd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# initializing model
class Customer(db.Model):
    __tablename__ = "customer"

    customer_id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    wallet_id = db.Column(db.String(64), nullable=False)

    def __init__ (self, customer_id, username, email, password, wallet_id):
        self.customer_id = customer_id
        self.username = username
        self.email = email
        self.password = password
        self.wallet_id = wallet_id

    def json(self):
        return {
            "customer_id": self.customer_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "wallet_id": self.wallet_id,
        }


@app.route("/customer")
def get_all():
    customers = Customer.query.all()
    if len(customers):
        return jsonify(
            {
                "code":200,
                "data": {
                    "customers": [
                        customer.json() for customer in customers
                    ]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no customers"
        }
    )
    

@app.route("/customer/<string:customer_id>")
def find_by_customer_id(customer_id):
    
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    if customer:
        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )

    return jsonify(
        {
            "code": "404",
            "message": "Customer does not exist."
        }
    )

# @app.route("/customer/<string:customer_id>", methods=["POST"])
# def create_customer(customer_id):
#     pass

if __name__ == "__main__":
    app.run(port=5000, debug=True)