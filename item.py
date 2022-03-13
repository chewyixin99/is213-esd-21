from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Flask SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/esd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# initializing model
class Item(db.Model):
    __tablename__ = "Item"

    item_id = db.Column(db.String(64), primary_key=True)
    hawker_id = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    cuisine_type = db.Column(db.String(64), nullable=False)
    base = db.Column(db.String(64), nullable=False)
    course_type = db.Column(db.String(64), nullable=False)

    def __init__ (self, item_id, hawker_id, description, price, cuisine_type, base, course_type):
        self.item_id = item_id
        self.hawker_id = hawker_id
        self.description = description
        self.price = price
        self.cuisine_type = cuisine_type
        self.base = base
        self.course_type = course_type

    def json(self):
        return {
            "item_id": self.item_id,
            "hawker_id": self.hawker_id,
            "description": self.description,
            "price": self.price,
            "cuisine_type": self.cuisine_type,
            "base": self.base,
            "course_type": self.cuisine_type,
        }


@app.route("/item")
def get_all():
    items = Item.query.all()
    if len(items):
        return jsonify(
            {
                "code":200,
                "data": {
                    "items": [
                        item.json() for item in items
                    ]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items"
        }
    )
    

@app.route("/item/<string:item_id>")
def find_by_item_id(item_id):
    
    item = Item.query.filter_by(item_id=item_id).first()
    if item:
        return jsonify(
            {
                "code": 200,
                "data": item.json()
            }
        )

    return jsonify(
        {
            "code": "404",
            "message": "Item does not exist."
        }
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)