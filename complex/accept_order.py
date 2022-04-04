from flask import Flask, request, jsonify
from flask_cors import CORS

# OS and error imports
import os, sys
from os import environ

# HTTP imports
import requests
from invokes import invoke_http

# # # AMQP imports
## switch the comments for the amqp path to test locally with (python <filename>.py)
# from amqp import amqp_setup # local path
import amqp_setup # compose version
import pika
import json

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

    old_order_data = old_order_result["data"]

    if old_order_result["code"] not in range(200, 300):

    # ##################### AMQP code      

    # handle error -> order retrieval fail

        print('\n\n-----Publishing the order retrieval error message with routing_key=retrieval.error-----')        

        message = {
            "code": 400,
            "message_type": "retrieval_error",
            "data": {
                "order_data": old_order_data,
            },
        }

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="retrieval.error", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        print("\nOrder retrieval error published to RabbitMQ Exchange.\n")

        # ##################### END OF AMQP code

        return old_order_result

        # ##################### AMQP code      

    # handle error -> order retrieval success

    print('\n\n-----Publishing the order retrieval notification message with routing_key=retrieval.notify-----')        

    message = {
        "code": 201,
        "message_type": "retrieval_notification",
        "data": {
            "order_data": old_order_data,
        },
    }

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="retrieval.notify", 
    body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    print("\nOrder retrieval notification published to RabbitMQ Exchange.\n")

    # ##################### END OF AMQP code

    if old_order_data["status"] == "pending":
        order_status = {
            "status": "accepted"
        }
        new_order_result = invoke_http(
            f"{order_url}/{order_id}",
            method="PUT",
            json=order_status
        )

        # ##################### AMQP code      
    
        # handle notification -> order acceptance successful

        print('\n\n-----Publishing the order accept notification message with routing_key=accept.notify-----')        

        new_order_data = new_order_result["data"]

        message = {
            "code": 201,
            "message_type": "accept_notification",
            "data": {
                "order_data": new_order_data,
            },
        }

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="accept.notify", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
    
        print("\nOrder accept notification published to RabbitMQ Exchange.\n")

        # ##################### END OF AMQP code

        return new_order_result

    # ##################### AMQP code      

    # handle error -> order acceptance fail

    print('\n\n-----Publishing the order accept error message with routing_key=accept.error-----')        

    new_order_data = new_order_result["data"]

    message = {
        "code": 400,
        "message_type": "accept_error",
        "data": {
            "order_data": new_order_data,
        },
    }

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="accept.error", 
    body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    print("\nOrder accept error published to RabbitMQ Exchange.\n")

    # ##################### END OF AMQP code

    return jsonify({
        "code": 403,
        "message": f"Unable to accept order. Order status is already {old_order_data['status']}."
    })

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5101, debug=True)