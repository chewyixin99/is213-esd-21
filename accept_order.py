from flask import Flask, request, jsonify
from flask_cors import CORS

# OS and error imports
import os, sys
from os import environ

# HTTP imports
import requests
from invokes import invoke_http

# AMQP imports
# import amqp_setup
# import pika
# import json

app = Flask(__name__)
CORS(app)

order_url = environ.get('order_URL') or "http://localhost:5004/order"

@app.route("/accept_order/<string:order_id>", methods=["POST"])
def accept_order(order_id):
    try:
        result = process_accept_order(order_id)
        return result

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = f"{str(e)} at {str(exc_type)}: {fname}: line {str(exc_tb.tb_lineno)}"
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": f"accept_order.py internal error: {ex_str}"
        })

def process_accept_order(order_id):

    old_order_result = invoke_http(
        f"{order_url}/{order_id}",
        method="GET"
    )
    if old_order_result["code"] not in range(200, 300):
        return old_order_result
        
    old_order_data = old_order_result["data"]
    if old_order_data["status"] == "pending":
        order_status = {
            "status": "accepted"
        }
        new_order_result = invoke_http(
            f"{order_url}/{order_id}",
            method="PUT",
            json=order_status
        )

        return new_order_result
    
    return jsonify({
        "code": 403,
        "message": f"Unable to accept order. Order status is already {old_order_data['status']}."
    })

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5101, debug=True)