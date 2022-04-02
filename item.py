from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Flask SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:root@localhost:3306/esd"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# initializing model
class Item(db.Model):
    __tablename__ = "Item"

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hawker_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    cuisine = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    course = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float, nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False, default=False)
    available = db.Column(db.Boolean, nullable=False, default=True)

    def __init__ (self, hawker_id, name, description, price, cuisine, course, vegetarian, available):
        self.hawker_id = hawker_id
        self.name = name
        self.cuisine = cuisine
        self.description = description
        self.course = course
        self.price = price
        self.vegetarian = vegetarian
        self.available = available

    def json(self):
        return {
            "item_id": self.item_id,
            "hawker_id": self.hawker_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "cuisine": self.cuisine,
            "course": self.course,
            "vegetarian": self.vegetarian,
            "available": self.available
        }

# Get all items
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
            "message": "No items found."
        }
    )

# Get specific item
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
            "message": f"Requested item (with item id {item_id}) does not exist."
        }
    )

# Get all items of a specific hawker
@app.route("/item/hawker/<string:hawker_id>")
def find_by_hawker_id(hawker_id):
    
    items = Item.query.filter_by(hawker_id=hawker_id).all()
    if items:
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
            "code": "404",
            "message": f"No items found for hawker {hawker_id}."
        }
    )

# Get all items of a specific cuisine
@app.route("/item/cuisine/<string:cuisine>")
def find_by_cuisine(cuisine):
    
    items = Item.query.filter_by(cuisine=cuisine).all()
    if items:
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
            "code": "404",
            "message": f"No {cuisine} cuisine items found."
        }
    )

# Get all items of a specific course
@app.route("/item/course/<string:course>")
def find_by_course(course):
    
    items = Item.query.filter_by(course=course).all()
    if items:
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
            "code": "404",
            "message": f"No {course} course items found."
        }
    )

# Get all vegetarian/non-vegetarian items
@app.route("/item/vegetarian/<int:vegetarian>")
def find_by_vegetarian(vegetarian):
    # Because URL Converter does not take boolean value - use int to represent
    if vegetarian: 
        items = Item.query.filter(Item.vegetarian.is_(True)).all()
    else:
        items = Item.query.filter(Item.vegetarian.is_(False)).all()

    if items:
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
            "code": "404",
            "message": f"No {'vegetarian' if vegetarian else 'non-vegetarian'} vegetarian items found."
        }
    )

# Create item
@app.route("/item/<int:hawker_id>", methods=["POST"])
def create_item(hawker_id):
    data = request.get_json()
    items = [Item(hawker_id, **row) for row in data['items']]

    try:
        db.session.add_all(items)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "items": [
                        item.json() for item in items
                    ]
                },
                "message": "An error occured while creating the item(s)"
            }
        )
    return jsonify(
        {
            "code": 201,
            "items": [
                item.json() for item in items
            ],
            "message": "Item(s) created."
        }
    )

# Update item
@app.route("/item/<int:item_id>", methods=['PUT'])
def update_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    if not (item):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "item_id": item_id
                },
                "message": f"Requested item (with item id {item_id}) does not exist."
            }
        ), 404

    data = request.get_json()

    try:
        for key in data.keys():            
            setattr(item, key, data[key])
        db.session.commit()
        
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "item_id": item_id
                },
                "message": "An error occurred while updating the item."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": item.json(),
            "message": "Successfully updated item."
        }
    ), 201

# Delete item
@app.route("/item/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.filter_by(item_id=item_id).first()
    if not (item):
        return jsonify(
            {
                "code": 404,
                "data": {
                    "item_id": item_id
                },
                "message": f"Requested item (with item id {item_id}) does not exist."
            }
        ), 404

    try:
        db.session.delete(item)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "item_id": item_id
                },
                "message": "An error occurred while deleting the item."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "item_id": item_id,
            "message": f"Successfully deleted item (with item id {item_id})."
        }
    ), 201



if __name__ == "__main__":
    app.run(port=5003, debug=True)