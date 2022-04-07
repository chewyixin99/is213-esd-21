# Flask imports
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

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
CORS(app, resources={r"/*": {"origins": "*"}})

order_url = environ.get('order_URL') or "http://localhost:5004/order"
wallet_url = environ.get('wallet_URL') or "http://localhost:5005/wallet"
escrow_url = environ.get('escrow_URL') or "http://localhost:5006/escrow"


@app.route("/place_order", methods=["POST"])
@cross_origin()
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
            # e.g. 
            # {
            #     "user_id": 1001,
            #     "hawker_id": 2010,
            #     "items": [{"item_id": 3100, "quantity": 3}, {"item_id": 3200, "quantity": 4}],
            #     "status": "pending",
            #     "total_price": 100,
            #     "discount": 0.0,
            #     "final_price": 100.0
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
    amqp_setup.check_setup()
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
        print("------------ WALLET UPDATED SUCCESSFULLY - {} ------------".format(wallet_update_result))
    else:
        order["status"] = "failed"
        print("------------ ORDER STATUS FAILED ------------")
        # ##################### AMQP code

        # # handle error -> wallet insufficient funds
        
        print('\n\n-----Publishing order status failed message with routing_key=order.error-----')
        message = {
            "code": 400,
            "message_type": "business_error",
            "data": "Insufficient wallet funds"
        }
        message = json.dumps(message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        print("\nOrder error - Insufficient wallet funds - published to the RabbitMQ Exchange:")

        ## Added this part to prevent code from continuing even when failed <-----------

        return wallet_data

        # ##################### END OF AMQP code

    # order microservice ---------------------------
    order_result = invoke_http(
        f"{order_url}",
        method="POST",
        json=order
    )
    order_data = order_result["data"]
    
    if order_result["code"] not in range(200,300):

        # ##################### AMQP code      
    
        # handle error -> order microservice error

        code = order_result["code"]
        
        print('\n\n-----Publishing the (order error) message with routing_key=order.error-----')

        message = {
            "code": 400,
            "message_type": "order_error",
            "data": order_data
        }

        message = json.dumps(message)
        
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
     
        print("\nOrder error - Code {} - published to the RabbitMQ Exchange:".format(code))
        return order_result

    # order_data = order_result["data"]
    # # handle notification -> order processed successfully

    # print('\n\n-----Publishing the order notification message with routing_key=order.notify-----')        

    # message = {
    #     "code": 201,
    #     "message_type": "order_notification",
    #     "data": {
    #         "order_data": order_data,
    #     },
    # }

    # message = json.dumps(message)

    # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.notify", 
    # body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    # print("\nOrder notification published to RabbitMQ Exchange.\n")

    # # ##################### END OF AMQP code


        

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
        escrow_data = escrow_result["data"]
        if escrow_result["code"] not in range(200,300):

            # ##################### AMQP code

            # handle error -> escrow was not processed successfully
            print('\n\n-----Publishing escrow failure message with routing_key=escrow.error-----')

            message = {
                "code": 400,
                "message_type": "escrow_error",
                "data": escrow_data
            }
            message = json.dumps(message)

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="escrow.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
            
            print("\nEscrow failed - Code {} - published to the RabbitMQ Exchange:".format(escrow_result["code"]))

            # ##################### end of AMQP code
            
            # delete_order_result = invoke_http(
            #     f"{order_url}/order/{order_data['order_id']}",
            #     method="DELETE",
            # )
            # return jsonify({
            #     "code": 409,
            #     "message": f"Cannot create escrow, order with order id {order_data['order_id']} deleted."
            # })
            return escrow_result

        else:

            # handle notification -> escrow was processed successfully

            print('\n\n-----Publishing the escrow notification message with routing_key=escrow.notify-----')        

            message = {
                "code": 400,
                "message_type": "escrow_notification",
                "data": escrow_data

            }

            message = json.dumps(message)

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="escrow.notify", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        
            print("\nOrder notification published to RabbitMQ Exchange.\n")

            # ##################### end of AMQP code


        # handle notification -> order processed successfully (moved all the way down to ensure escrow is successful before sending notification)

        print('\n\n-----Publishing the order notification message with routing_key=order.notify-----')        

        message = {
            "code": 201,
            "message_type": "order_notification",
            "data": order_data
        }

        message = json.dumps(message)

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.notify", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        print("\nOrder notification published to RabbitMQ Exchange.\n")

        # ##################### END OF AMQP code

    # notification microservice ---------------------------

    # error microservice ---------------------------

        print("Escrow successfully created -----------------------")
       
        return escrow_result
           
    return order_result
    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
