from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Escrow(db.Model):
    __tablename__ = 'escrow'

    order_id = db.Column(db.Integer, primary_key=True)
    payer_id = db.Column(db.Integer, nullable=False)
    receiving_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    def __init__(self, order_id, payer_id, receiving_id, amount):
        self.order_id = order_id
        self.payer_id = payer_id
        self.receiving_id = receiving_id
        self.amount = amount


    def json(self):
        return {
            "order_id": self.order_id,
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
            "message": "No escrow records found."
        }
    ), 404


# retrieve escrow by id
@app.route("/escrow/<int:order_id>")
def find_by_order_id(order_id):
    escrow = Escrow.query.filter_by(order_id=order_id).first()
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
            "message": f"Requested escrow record (order id {order_id}) does not exist."
        }
    ), 404


#create escrow (only positive values, remember!)
@app.route("/escrow/<int:order_id>", methods=['POST'])
def create_escrow(order_id):
    if (Escrow.query.filter_by(order_id=order_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "order_id": order_id
                },
                "message": f"Escrow record for this order_id ({order_id}) already exists."
            }
        ), 400

    data = request.get_json()
    escrow = Escrow(order_id, **data) #need to revise this, creation has error

    try:
        db.session.add(escrow)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "order_id": order_id
                },
                "message": "An error occurred while creating the escrow record."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": escrow.json(),
            "message": f"Escrow successfully created for order {order_id}."
        }
    ), 201



#delete escrow
@app.route("/escrow/<int:order_id>", methods=['DELETE'])
def delete_escrow(order_id):
    escrow = Escrow.query.filter_by(order_id=order_id).first()
    if not (escrow):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "order_id": order_id
                },
                "message": f"No escrow record of {order_id} found."
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
                    "order_id": order_id
                },
                "message": "An error occurred deleting the escrow."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "order_id": order_id
        },
        "message": f"Successfully deleted item (with order id {order_id})."
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)