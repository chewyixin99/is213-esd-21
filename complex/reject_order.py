# Flask imports
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
wallet_url = environ.get('wallet_URL') or "http://localhost:5005/wallet"
escrow_url = environ.get('escrow_URL') or "http://localhost:5006/escrow"

@app.route("/reject_order/<string:order_id>", methods=["POST"])
def reject_order(order_id):
    try:
        return process_reject_order(order_id)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = f"{str(e)} at {str(exc_type)}: {fname}: line {str(exc_tb.tb_lineno)}"
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": f"reject_order.py internal error: {ex_str}"
        })

def process_reject_order(order_id):
    
    # order microservice ----------------------------
    old_order_result = invoke_http(
        f"{order_url}/{order_id}",
        method="GET"
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
    if old_order_result["code"] not in range(200,300):
        # -------------------- FOR JIAN LIN TO ADD AMQP FAIL

        # ##################### AMQP code      
    
        # handle error -> order retrieval fail

        print('\n\n-----Publishing order retrieval error message with routing_key=retrieval.error-----')        

        message = {
            "code": 400,
            "message_type": "retrieval_error",
            "data": old_order_result,
        }
        message = json.dumps(message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="retrieval.error", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
    
        print("\nOrder retrieval error published to RabbitMQ Exchange.\n")

        # ##################### END OF AMQP code

        return old_order_result
    
    # -------------------- FOR JIAN LIN TO ADD AMQP PASS

    # ##################### AMQP code      

    # handle notification -> order retrieveal successful

    print('\n\n-----Publishing the order retrieval notification message with routing_key=retrieval.notify-----')        

    old_order_data = old_order_result["data"]

    message = {
        "code": 201,
        "message_type": "retrieval_notification",
        "data": old_order_data
    }
    message = json.dumps(message)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="retrieval.notify", 
    body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    print("\nOrder retrieval notification published to RabbitMQ Exchange.\n")

    # ##################### END OF AMQP code

    if old_order_data["status"] == "pending":
        # escrow microservice ----------------------------
        # get data of $ in escrow
        escrow_result = invoke_http(
            f"{escrow_url}/{old_order_data['order_id']}",
            method="GET"
        )

        if escrow_result["code"] not in range(200,300):
            # -------------------- FOR JIAN LIN TO ADD AMQP FAIL

            # ##################### AMQP code      

            # handle error -> escrow processing fail

            print('\n\n-----Publishing the escrow error message with routing_key=escrow.error-----')        

            
            message = {
                "code": 400,
                "message_type": "escrow_error",
                "data": escrow_result
            }
            message = json.dumps(message)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="escrow.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            print("\nOrder escrow error published to RabbitMQ Exchange.\n")

            # ##################### END OF AMQP code

            return escrow_result
        
        escrow_data = escrow_result["data"]
        
        # # -------------------- FOR JIAN LIN TO ADD AMQP PASS

        # ##################### AMQP code      

        # handle notify -> escrow processing notification

        print('\n\n-----Publishing the escrow notification message with routing_key=escrow.notify-----')        

        message = {
            "code": 201,
            "message_type": "escrow_notification",
            "data": escrow_data
        }
        message = json.dumps(message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="escrow.notify", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        print("\nOrder escrow notification published to RabbitMQ Exchange.\n")

        # ##################### END OF AMQP code

        escrow_amount = escrow_result["data"]["amount"]
        # wallet microservice ----------------------------
        # return money to user
        wallet_update_json = {
            "amount_to_add_to_available_balance": escrow_amount,
            "amount_to_add_to_total_balance": 0
        }
        wallet_result = invoke_http(
            f"{wallet_url}/{old_order_data['user_id']}",
            method="PUT",
            json=wallet_update_json
        )

        if wallet_result["code"] not in range(200,300):
            # -------------------- FOR JIAN LIN TO ADD AMQP FAIL

            # ##################### AMQP code      

            # handle error -> wallet processing fail

            print('\n\n-----Publishing the wallet error message with routing_key=wallet.error-----')        

            message = {
                "code": 400,
                "message_type": "wallet_error",
                "data": wallet_result
                
            }
            message = json.dumps(message)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="wallet.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            print("\nOrder wallet error published to RabbitMQ Exchange.\n")

            # ##################### END OF AMQP code

            return wallet_result

        wallet_data = wallet_result["data"]
        
        # -------------------- FOR JIAN LIN TO ADD AMQP PASS

        # ##################### AMQP code      

        # handle notification -> wallet processing successful

        print('\n\n-----Publishing the wallet notification message with routing_key=wallet.notify-----')        

        message = {
            "code": 201,
            "message_type": "wallet_notification",
            "data": wallet_data
        }
        message = json.dumps(message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="wallet.notify", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        print("\nWallet notification published to RabbitMQ Exchange.\n")

        # ##################### END OF AMQP code

        escrow_delete_result = invoke_http(
            f"{escrow_url}/{old_order_data['order_id']}",
            method="DELETE"
        )

        if escrow_delete_result["code"] not in range(200,300):
            # -------------------- FOR JIAN LIN TO ADD AMQP FAIL

            # ##################### AMQP code      

            # handle error -> escrow deletion fail

            print('\n\n-----Publishing the escrow deletion error message with routing_key=escrow_deletion.error-----')        

            message = {
                "code": 400,
                "message_type": "escrow_deletion_error",
                "data": escrow_delete_result
            }
            message = json.dumps(message)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="escrow_deletion.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            print("\nEscrow deletion error published to RabbitMQ Exchange.\n")

            # ##################### END OF AMQP code

            return escrow_delete_result

        # -------------------- FOR JIAN LIN TO ADD AMQP PASS
        escrow_delete_data = escrow_delete_result["data"]

        # ##################### AMQP code      

        # handle notification -> rejection successful

        print('\n\n-----Publishing the escrow deletion notification message with routing_key=escrow_deletion.notify-----')        

        message = {
            "code": 201,
            "message_type": "escrow_deletion_notification",
            "data": escrow_delete_data
        }
        message = json.dumps(message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="escrow_deletion.notify", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        print("\nEscrow deletion notification published to RabbitMQ Exchange.\n")

        # ##################### END OF AMQP code

        order_status = {
            "status": "rejected"
        }
        new_order_result = invoke_http(
            f"{order_url}/{order_id}",
            method="PUT",
            json=order_status
        )

        if new_order_result["code"] not in range(200,300):
            # -------------------- FOR JIAN LIN TO ADD AMQP FAIL

            # ##################### AMQP code      

            # handle error -> order rejection fail

            print('\n\n-----Publishing the order rejection error message with routing_key=reject.error-----')        

            message = {
                "code": 400,
                "message_type": "reject_error",
                "data": new_order_result
            }
            message = json.dumps(message)
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="reject.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            print("\nOrder rejection error published to RabbitMQ Exchange.\n")

            # ##################### END OF AMQP code

            return new_order_result

        new_order_data = new_order_result["data"]
        # -------------------- FOR JIAN LIN TO ADD AMQP PASS

        # ##################### AMQP code      

        # handle notification -> order rejection success

        print('\n\n-----Publishing the order rejection notification message with routing_key=reject.notify-----')        


        message = {
            "code": 201,
            "message_type": "reject_notification",
            "data": new_order_data
        }
        message = json.dumps(message)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="reject.notify", 
        body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

        print("\nOrder rejection notification published to RabbitMQ Exchange.\n")

        return new_order_data

        # ##################### END OF AMQP code


    # -------------------- FOR JIAN LIN TO ADD AMQP FAIL IF STATUS NOT PENDING

    # ##################### AMQP code      

    # handle error -> order rejection status error

    print('\n\n-----Publishing the order rejection status error message with routing_key=reject_status.error-----')        

    message = {
        "code": 403,
        "message_type": "reject_status_error",
        "data": old_order_data
    }
    message = json.dumps(message)
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="reject_status.error", 
    body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    print("\nOrder rejection status error published to RabbitMQ Exchange.\n")

    # ##################### END OF AMQP code

    return jsonify({
        "code": 403,
        "message": f"Unable to reject order. Order status is already {old_order_data['status']}."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5102, debug=True)
