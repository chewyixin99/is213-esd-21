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
import amqp_setup
import pika
import json

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
            # return jsonify(result), result["code"]

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

    # check AMQP connection - if not active, activate it
    amqp_setup.check_setup()


    # wallet microservice ---------------------------
    # get balance of user
    wallet_result = invoke_http(
        f"{wallet_url}/{order['user_id']}",
        method="GET"
    )
        # wallet_result return format
            # {
            #     "code": int,
            #     "data": {
            #         "available_balance": float,
            #         "total_balance": float,
            #         "wallet_id": int,
            #     }
            # }
    wallet_data = wallet_result["data"]
    #! validation check: available_balance >= order["final_price"]
    available_balance = wallet_data["available_balance"]
    if available_balance >= order["final_price"]:
        order["status"] = "pending"

    else:
        order["status"] = "failed"

        # handle business error

        print('\n\n-----Publishing order status failed message with routing_key=order.error-----')
        
        message = {
            "code": 400,
            "message_type": "business_error",
            "data": {
                "order_data": "Insufficient wallet funds",
            },
        }

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        
        print("\nOrder error - Insufficient wallet funds - published to the RabbitMQ Exchange:")


    
    # order microservice ---------------------------
    order_result = invoke_http(
        f"{order_url}",
        method="POST",
        json=order
    )
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
    
    # handle programming error

    code = order_result["code"]
    order_id = order_data["order_id"]

    if code not in range(200, 300):

        print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

        message = {
            "code": 400,
            "message_type": "order_error",
            "data": {
                "order_data": order_data,
            },
        }

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
        print("\nOrder error - Code {} - published to the RabbitMQ Exchange:".format(code))

    else:
        print('\n\n-----Publishing the order notification message with routing_key=order.notify-----')        

        # message = "\nOrder ID: {} is sent to the kitchen.. Please wait for confirmation. Thank you".format(order_id)

        message = {
            "code": 400,
            "message_type": "order_notification",
            "data": {
                "order_data": order_data,
            },
        }

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.notify", 
        body=message,  properties=pika.BasicProperties(delivery_mode = 2)) 
    
        print("\nOrder notification published to RabbitMQ Exchange.\n")


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
        # sample escrow_result return format
            # {
            #     "code": 201,
            #     "data": {
            #         "amount": 10.0,
            #         "order_id": 4010,
            #         "payer_id": 1001,
            #         "receiving_id": 2000,
            #         "time": "Fri, 01 Apr 2022 11:45:53 GMT"
            #     }
            # }

       
        # handle programming error

        escrow_data = escrow_result["data"]

        if escrow_result['code'] not in range(200, 300):

            print('\n\n-----Publishing escrow failure message with routing_key=escrow.error-----')
            
            # message = 'Escrow failed - Code {}.'.format(code)

            message = {
                "code": 400,
                "message_type": "escrow_error",
                "data": {
                    "order_data": escrow_data,
                },
            }   

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="escrow.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
            
            print("\nEscrow failed - Code {} - published to the RabbitMQ Exchange:".format(code))

        else:
            print('\n\n-----Publishing the escrow notification message with routing_key=escrow.notify-----')        

            # message = "\nOrder ID: {} is sent to the kitchen.. Please wait for confirmation. Thank you".format(order_id)

            message = {
                "code": 400,
                "message_type": "escrow_notification",
                "data": {
                    "order_data": escrow_data,
                },
            }


            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="escrow.notify", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        
            print("\nOrder notification published to RabbitMQ Exchange.\n")


    # notification microservice ---------------------------

    # error microservice ---------------------------

    return order_result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
