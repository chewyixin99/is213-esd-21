# Flask imports
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
escrow_url = environ.get('escrow_URL') or "http://localhost:5006/escrow"
wallet_url = environ.get('wallet_URL') or "http://localhost:5005/wallet"

@app.route("/complete_order/<string:order_id>", methods=["POST"])
def complete_order(order_id):

    try:
        return process_complete_order(order_id)
    
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = f"{str(e)} at {str(exc_type)}: {fname}: line {str(exc_tb.tb_lineno)}"
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": f"accept_order.py internal error: {ex_str}"
        })


def process_complete_order(order_id):

    # order microservice ----------------------------
    # check the status
    old_order_result = invoke_http(
        f"{order_url}/{order_id}",
        method="GET"
    )
    if old_order_result["code"] not in range(200,300):
        return old_order_result
    
    # get $ data from the order
    old_order_data = old_order_result["data"]
    # example order_result return format
        # {
        #     "code": 201,
        #     "data": {
        #         "discount": 0.0,
        #         "final_price": 10.0,
        #         "hawker_id": 2000,
        #         "items": "[{'item_id': 3000,'quantity' : 1 }]",
        #         "order_id": 4003,
        #         "status": "pending",
        #         "time": "Fri, 01 Apr 2022 11:09:40 GMT",
        #         "total_price": 10.0,
        #         "user_id": 1001
        #     },
        #     "message": "Created order."
        # }

    # check status is accepted
    if old_order_data["status"] != "accepted":
        return jsonify({
        "code": 403,
        "message": f"Unable to complete order. Order status is already {old_order_data['status']}."
    })

    # escrow microservice ----------------------------
    # check if escrow exists
    escrow_result = invoke_http(
        f"{escrow_url}/{old_order_data['order_id']}",
        method="GET"
    )
    if escrow_result["code"] not in range(200,300):
        return escrow_result
        
    price_to_update = escrow_result["data"]["amount"]

    # wallet microservice ----------------------------
    # transfer money to hawker (total and available)
    hawker_wallet_update_json = {
        "amount_to_add_to_available_balance": price_to_update,
        "amount_to_add_to_total_balance": price_to_update
    }
    user_wallet_update_json = {
        "amount_to_add_to_available_balance": 0,
        "amount_to_add_to_total_balance": -price_to_update
    }
    hawker_wallet_result = invoke_http(
        f"{wallet_url}/{old_order_data['hawker_id']}",
        method="PUT",
        json=hawker_wallet_update_json
    )
    if hawker_wallet_result["code"] not in range(200,300):
        return hawker_wallet_result

    # deduct money from user (total)
    user_wallet_result = invoke_http(
        f"{wallet_url}/{old_order_data['user_id']}",
        method="PUT",
        json=user_wallet_update_json
    )
    if user_wallet_result["code"] not in range(200,300):
        return user_wallet_result

    # escrow microservice ----------------------------
    # delete escrow once done
    escrow_delete_result = invoke_http(
        f"{escrow_url}/{order_id}",
        method="DELETE"
    )
    if escrow_delete_result["code"] not in range(200,300):
        return escrow_delete_result
    
    # finally, update order status to completed
    order_status = {
        "status": "completed"
    }

    new_order_result = invoke_http(
        f"{order_url}/{order_id}",
        method="PUT",
        json=order_status
    )
    if new_order_result["code"] not in range(200,300):
        return new_order_result


    return new_order_result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5103, debug=True)
