from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Wallet(db.Model):
    __tablename__ = 'wallet'

    wallet_id = db.Column(db.Integer, primary_key=True)
    total_balance = db.Column(db.Float, nullable=False)
    available_balance = db.Column(db.Float, nullable=False)

    def __init__(self, wallet_id, total_balance, available_balance):
        self.wallet_id = wallet_id
        self.total_balance = total_balance
        self.available_balance = available_balance

    def json(self):
        return {
            "wallet_id": self.wallet_id,
            "total_balance": self.total_balance,
            "available_balance": self.available_balance}


# retrieve all wallets
@app.route("/wallet")
def get_all():
    walletlist = Wallet.query.all()
    if len(walletlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "wallets": [wallet.json() for wallet in walletlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No wallets found."
        }
    ), 404


# retrieve wallet by id
@app.route("/wallet/<int:wallet_id>")
def find_by_wallet_id(wallet_id):
    wallet = Wallet.query.filter_by(wallet_id=wallet_id).first()
    if wallet:
        return jsonify(
            {
                "code": 200,
                "data": wallet.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": f"Requested wallet {wallet_id} does not exist."
        }
    ), 404


#create wallet
@app.route("/wallet/<int:wallet_id>", methods=['POST'])
def create_wallet(wallet_id):
    if (Wallet.query.filter_by(wallet_id=wallet_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "wallet_id": wallet_id
                },
                "message": f"Wallet for this wallet_id {wallet_id} already exists."
            }
        ), 400

    data = request.get_json()
    wallet = Wallet(wallet_id, **data)

    try:
        db.session.add(wallet)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "wallet_id": wallet_id
                },
                "message": "An error occurred creating the wallet."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": wallet.json()
        }
    ), 201


#add amount to wallet, can be in negative integers to simulate a deduction
@app.route("/wallet/<int:wallet_id>", methods=['PUT'])
def add_amount_to_wallet(wallet_id):
    wallet = Wallet.query.filter_by(wallet_id=wallet_id).first()
    if not (wallet):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "wallet_id": wallet_id
                },
                "message": f"Wallet {wallet_id} does not exist to be updated."
            }
        ), 404

    data = request.get_json()

    try:
        # data will come in 2 parts to be settled by each complex microservice.
        # (place_order will update only user's AB, reject_order will update both user's AB & TB, complete_order will update user+hawker's AB & TB)
        wallet.available_balance += data['amount_to_add_to_available_balance']
        wallet.total_balance += data['amount_to_add_to_total_balance']
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "wallet_id": wallet_id
                },
                "message": f"An error occurred updating the wallet {wallet_id}."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": wallet.json()
        }
    ), 201


#delete wallet
@app.route("/wallet/<int:wallet_id>", methods=['DELETE'])
def delete_wallet(wallet_id):
    wallet = Wallet.query.filter_by(wallet_id=wallet_id).first()
    if not (wallet):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "wallet_id": wallet_id
                },
                "message": f"No wallet of {wallet_id} found."
            }
        ), 404

    try:
        db.session.delete(wallet)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "wallet_id": wallet_id
                },
                "message": "An error occurred deleting the wallet."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "wallet_id": wallet_id
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)