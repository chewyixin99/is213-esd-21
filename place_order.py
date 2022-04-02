# Flask imports
from flask import Flask, request, jsonify
from flask_cors import CORS

# OS and error imports
import os, sys
from os import environ

# HTTP imports
import requests
from invokes import invoke_http

# # AMQP imports
# import amqp_setup
# import pika
# import json

app = Flask(__name__)
CORS(app)

order_url = environ.get('order_URL') or "http://localhost:5004/order"
escrow_url = environ.get('escrow_URL') or "http://localhost:5006/escrow"
wallet_url = environ.get('wallet_URL') or "http://localhost:5005/wallet"


@app.route("/place_order", methods=["POST"])
def place_order():
    if request.is_json:
        try:
            # order format
            # {
            #     'user_id': int
            #     'hawker_id': int,
            #     'items': json_string - array of objects e.g. [{'item_id': ..., 'quantity': ...}, {...}],
            #     'status': "",
            #     'total_price': float,
            #     'discount': float
            #     'final_price': float,
            # }
            order = request.get_json()
            result = process_place_order(order)

            return result

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = f"{str(e)} at {str(exc_type)}: {fname}: line {str(exc_tb.tb_lineno)}"
            print(ex_str)
        
            return jsonify({
                "code": 500,
                "message": f"place_order.py internal error: {ex_str}" 
            })


    return jsonify({
        "code": 400,
        "message": f"Invalid JSON input {requests.request.get_data()}"
    })

def process_place_order(order):
    # order format
            # {
            #     'user_id': int
            #     'hawker_id': int,
            #     'items': json_string - array of objects e.g. [{'item_id': ..., 'quantity': ...}, {...}],
            #     'status': string,
            #     'total_price': float,
            #     'discount': float
            #     'final_price': float,
            # }

    # ##################### AMQP code
    # # check AMQP connection - if not active, activate it
    # amqp_setup.check_setup()
    # ##################### end of AMQP code

    # wallet microservice ---------------------------
    # get balance of user
    wallet_result = invoke_http(
        f"{wallet_url}/{order['user_id']}",
        method="GET"
    )
    if wallet_result["code"] not in range(200,300):
        return wallet_result

    wallet_data = wallet_result["data"]
    # wallet_result return format
        # {
        #     "code": int,
        #     "data": {
        #         "available_balance": float,
        #         "total_balance": float,
        #         "wallet_id": int,
        #     }
        # }
    #! validation check: available_balance >= order["final_price"]
    available_balance = wallet_data["available_balance"]
    if available_balance >= order["final_price"]:
        order["status"] = "pending"
        wallet_update_json = {
            "amount_to_add_to_available_balance": -order["final_price"],
            "amount_to_add_to_total_balance": 0
        }
        wallet_update_result = invoke_http(
            f"{wallet_url}/{order['user_id']}",
            method="PUT",
            json=wallet_update_json
        )

        if wallet_update_result["code"] not in range(200,300):
            return wallet_update_result

    else:
        order["status"] = "failed"

        # ##################### AMQP code
        # # handle business error
        # print('\n\n-----Publishing order status failed message with routing_key=order.error-----')
        # message = {
        #     "code": 400,
        #     "message_type": "business_error",
        #     "data": {
        #         "order_data": "Insufficient wallet funds",
        #     },
        # }
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
        # body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # print("\nOrder error - Insufficient wallet funds - published to the RabbitMQ Exchange:")
        # ##################### END OF AMQP code

    # order microservice ---------------------------
    order_result = invoke_http(
        f"{order_url}",
        method="POST",
        json=order
    )
    if order_result["code"] not in range(200,300):

        # ##################### AMQP code
        # # handle programming error
        # order_id = order["order_id"]
        # print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

        # message = {
        #     "code": 400,
        #     "message_type": "order_error",
        #     "data": {
        #         "order_data": order,
        #     },
        # }
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
        # body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # print("\nOrder error - Code {} - published to the RabbitMQ Exchange:".format(order_result["code"]))
        # ##################### END OF AMQP code

        return order_result
        
    # ##################### AMQP code
    # print('\n\n-----Publishing the order notification message with routing_key=order.notify-----')        
    # # message = "\nOrder ID: {} is sent to the kitchen.. Please wait for confirmation. Thank you".format(order_id)
    # message = {
    #     "code": 400,
    #     "message_type": "notification",
    #     "data": {
    #         "order_data": order,
    #     },
    # }
    # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.notify", 
    # body=message)
    # print("\nOrder notification published to RabbitMQ Exchange.\n")
    # ##################### end of AMQP code

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

    order_data = order_result["data"]
    # escrow microservice ---------------------------
    #! validation check: if order["status"]="pending", create escrow and extract payment from user, else don't escrow
    if order["status"] == "pending":
        escrow_json = {
            "payer_id": order_data["user_id"],
            "receiving_id": order_data["hawker_id"],
            "amount": order_data["final_price"],
        }
        escrow_result = invoke_http(
            f"{escrow_url}/{order_data['order_id']}",
            method="POST",
            json=escrow_json
        )
        if escrow_result["code"] not in range(200,300):

            # ##################### AMQP code
            # print('\n\n-----Publishing escrow failure message with routing_key=escrow.error-----')
            # # message = 'Escrow failed - Code {}.'.format(escrow_result["code"])
            # message = {
            #     "code": 400,
            #     "message_type": "escrow_error",
            #     "data": {
            #         "order_data": escrow_data,
            #     },
            # }   
            # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="escrow.error", 
            # body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
            
            # print("\nEscrow failed - Code {} - published to the RabbitMQ Exchange:".format(escrow_result["code"]))
            # ##################### end of AMQP code

            return escrow_result

        print("Escrow successfully created -----------------------")
       
        # handle programming error
        # ##################### AMQP code
        # print('\n\n-----Publishing the order notification message with routing_key=order.notify-----')        
        # # message = "\nOrder ID: {} is sent to the kitchen.. Please wait for confirmation. Thank you".format(order_id)
        # message = {
        #     "code": 400,
        #     "message_type": "notification",
        #     "data": {
        #         "order_data": order_data,
        #     },
        # }
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.notify", 
        #     body=message)
        # print("\nOrder notification published to RabbitMQ Exchange.\n")
        # ##################### end of AMQP code

        return escrow_result
           
    return order_result
    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
