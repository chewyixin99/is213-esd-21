from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)

# Flask SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost:3306/esd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# initializing model
class Order(db.Model):
    __tablename__ = "Order"

    order_id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    hawker_id = db.Column(db.String(64), nullable=False)
    time = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    status = db.Column(db.String(10), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    final_price = db.Column(db.Float, nullable=False)
    items = db.Column(db.String(255), nullable=False)
    

    def __init__ (self, order_id, user_id, hawker_id, status, total_price, discount, final_price, items):
        self.order_id = order_id
        self.user_id = user_id
        self.hawker_id = hawker_id
        self.time = time
        self.status = status
        self.total_price = total_price
        self.discount = discount
        self.final_price = final_price

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



if __name__ == "__main__":
    app.run(port=5004, debug=True)