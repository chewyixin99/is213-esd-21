from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS
from os import environ

app = Flask(__name__)

# Flask SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('dbURL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)


# initializing model
class Order(db.Model):
    __tablename__ = "Order"

    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    hawker_id = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    status = db.Column(db.String(10), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    final_price = db.Column(db.Float, nullable=False)
    items = db.Column(db.String(255), nullable=False)
    

    def __init__ (self, user_id, hawker_id, status, total_price, discount, final_price, items):
        self.user_id = user_id
        self.hawker_id = hawker_id
        self.status = status
        self.total_price = total_price
        self.discount = discount
        self.final_price = final_price
        self.items = items

    def json(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "hawker_id": self.hawker_id,
            "time": self.time,
            "status": self.status,
            "total_price": self.total_price,
            "discount": self.discount,
            "final_price": self.final_price,
            "items": self.items,
        }


@app.route("/order")
def get_all():
    orders = Order.query.all()
    if len(orders):
        return jsonify(
            {
                "code":200,
                "data": {
                    "orders": [
                        order.json() for order in orders
                    ]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no orders"
        }
    )

# Get order by order id
@app.route("/order/<string:order_id>")
def find_by_order_id(order_id):
    # .first() is similar to LIMIT 1 clause in SQL
    # .filter_by is similar to WHERE clause in SQL
    order = Order.query.filter_by(order_id=order_id).first()
    if order:
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        )
    return jsonify(
        {
            "code": 400,
            "message": f"Order with order id:'{order_id}' not found."
        }
    )


# Get order by user_id
@app.route("/order/user/<string:user_id>")
def find_by_user_id(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    if len(orders):
        return jsonify(
            {
                "code":200,
                "data": {
                    "orders": [
                        order.json() for order in orders
                    ]
                }
            }
        )
    return jsonify(
        {
            "code": 400,
            "message": f"Order with user id:{user_id} not found."
        }
    )


# Get order by hawker id
@app.route("/order/hawker/<string:hawker_id>")
def find_by_hawker_id(hawker_id):
    orders = Order.query.filter_by(hawker_id=hawker_id).all()
    if len(orders):
        return jsonify(
            {
                "code":200,
                "data": {
                    "orders": [
                        order.json() for order in orders
                    ]
                }
            }
        )
    return jsonify(
        {
            "code": 400,
            "message": f"Order with hawker id:{hawker_id} not found."
        }
    )

@app.route("/order/hawker/<string:hawker_id>/<string:status>")
def find_by_hawker_id_by_status(hawker_id, status):
    orders = Order.query.filter_by(
        hawker_id=hawker_id,
        status=status
    ).all()
    
    if len(orders):
        return jsonify(
            {
                "code":200,
                "data": {
                    "orders": [
                        order.json() for order in orders
                    ]
                }
            }
        )
    return jsonify(
        {
            "code": 400,
            "message": f"Order with hawker id:{hawker_id} and status:{status} not found."
        }
    )


# Create a order record
@app.route("/order", methods=["POST"])
def create_order():
    data = request.get_json()
    order = Order(**data)

    try:
        db.session.add(order)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "order": order,
                },
                "message": "An error occurred while creating order"
            }
        )
    return jsonify(
        {
            "code": 201,
            "data": order.json(),
            "message": f"Created order, status:{order.json()['status']}."
        }
    )


# Edit an order status
@app.route("/order/<string:order_id>", methods=["PUT"])
def update_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if (order):
        data = request.get_json()
        order.status = data['status']
                
        try:
            db.session.merge(order)
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": order.json(),
                    "message": f"Successfully updated order {order.order_id} status to: {data['status']}."
                }
            )
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "order": order
                    },
                    "message": "An error occured updating the order."
                }
            )
    return jsonify(
        {
            "code": 404,
            "data": {
                "order": order
            },
            "message": f"Order {order_id} not found."

        }
    )

# delete order
@app.route("/order/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not (order):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "order_id": order_id
                },
                "message": f"Requested Order (with item id {order_id}) does not exist."
            }
        )
    try:
        db.session.delete(order)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "order_id": order_id
                },
                "message": "An error occurred while deleting the order."
            }
        ),
    return jsonify(
        {
            "code": 201,
            "order_id": order_id,
            "message": f"Successfully deleted item (with order id {order_id})."
        }
    )




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004, debug=True)