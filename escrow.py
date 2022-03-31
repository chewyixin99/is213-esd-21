from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/esd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Escrow(db.Model):
    __tablename__ = 'escrow'

    escrow_id = db.Column(db.Integer, primary_key=True)
    payer_id = db.Column(db.Integer, nullable=False)
    receiving_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    def __init__(self, escrow_id, payer_id, receiving_id, amount, time):
        self.escrow_id = escrow_id
        self.payer_id = payer_id
        self.receiving_id = receiving_id
        self.amount = amount
        self.time = time


    def json(self):
        return {
            "escrow_id": self.escrow_id,
            "payer_id": self.payer_id,
            "receiving_id": self.receiving_id,
            "amount": self.amount,
            "time": self.time}


# retrieve all escrows
@app.route("/escrow")
def get_all():
    escrowlist = Escrow.query.all()
    if len(escrowlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "escrows": [escrow.json() for escrow in escrowlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No escrows found."
        }
    ), 404


# retrieve escrow by id
@app.route("/escrow/<int:escrow_id>")
def find_by_escrow_id(escrow_id):
    escrow = Escrow.query.filter_by(escrow_id=escrow_id).first()
    if escrow:
        return jsonify(
            {
                "code": 200,
                "data": escrow.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "escrow not found."
        }
    ), 404


#create escrow (only positive values, remember!)
@app.route("/escrow/<int:escrow_id>", methods=['POST'])
def create_escrow(escrow_id):
    if (Escrow.query.filter_by(escrow_id=escrow_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "escrow_id": escrow_id
                },
                "message": "escrow for this order_id already exists."
            }
        ), 400

    data = request.get_json()
    escrow = Escrow(escrow_id, **data)

    try:
        db.session.add(escrow)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "escrow_id": escrow_id
                },
                "message": "An error occurred creating the escrow."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": escrow.json()
        }
    ), 201



#delete escrow
@app.route("/escrow/<int:escrow_id>", methods=['DELETE'])
def delete_escrow(escrow_id):
    escrow = E  scrow.query.filter_by(escrow_id=escrow_id).first()
    if not (escrow):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "escrow_id": escrow_id
                },
                "message": "escrow not found."
            }
        ), 404

    try:
        db.session.delete(escrow)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "escrow_id": escrow_id
                },
                "message": "An error occurred deleting the escrow."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "escrow_id": escrow_id
        }
    ), 201


if __name__ == '__main__':
    app.run(port = 5006, debug = True)