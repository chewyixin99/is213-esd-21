import json
import os
from twilio.rest import Client
import amqp_setup

monitorBindingKey='*.notify'
account_sid = 'ACfb66da0927db664980a680736cc0e708'
auth_token = '681ddb63eacac9a192280a59fedec821'
twilio_number = '+15857284607'
target_number = '+6586862106'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'Notification'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    # it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an notification log by " + __file__)
    processNotificationLog(body)
    print() # print a new line feed

def processNotificationLog(notificationBody):


    client = Client(account_sid, auth_token)

    loaded_body = json.loads(notificationBody)
    message_type = loaded_body['message_type']
    data = loaded_body["data"]["order_data"]
    body = ""

    if loaded_body['message_type'] == "order_notification":

        body = "\n"
        body += "\nHello User {}, your order {} is sent to the kitchen. \n\nDetails are as follows:\n".format(data["user_id"],data["order_id"])
        body += "\n--------------"
        body += "\nHawker ID: {}".format(data["hawker_id"])
        body += "\nItems:\n"
        
        for item in data["items"]:
            body += "Item ID: {}, Qty: {}\n".format(item["item_id"],item["quantity"])

        body += "\nTotal Price: ${}".format(data["total_price"])
        body += "\nDiscount: ${}".format(data["discount"])
        body += "\nFinal Price: ${}".format(data["final_price"])
        body += "\n--------------"
        body += "\nTime of Order: {}".format(data["time"])
        

    elif loaded_body['message_type'] == "accept_notification":
        body = "\n"
        body += "\nHello User {}, your order {} is being processed.\n".format(data["user_id"],data["order_id"])
        body += "\n--------------"
        body += "\nHawker ID: {}".format(data["hawker_id"])
        body += "\nItems:\n"
        
        for item in data["items"]:
            body += "Item ID: {}, Qty: {}\n".format(item["item_id"],item["quantity"])

        body += "\n--------------"
        body += "\nTime of Order: {}".format(data["time"])

    elif loaded_body['message_type'] == "order_completion_notification":
        body = "\n"
        body += "\nHello User {}, your order {} is completed.\n\nPayment details are as follows:".format(data["user_id"],data["order_id"])
        body += "\n--------------"
        body += "\nTotal Price: ${}".format(data["total_price"])
        body += "\nDiscount: ${}".format(data["discount"])
        body += "\nFinal Price: ${}".format(data["final_price"])
        body += "\n--------------"
        body += "\nTime of Order: {}".format(data["time"])
    
    if body != "":
        client.messages.create(
            body=body,
            from_=twilio_number,
            to=target_number
        )
        print("Notification: {} sent successfully..".format(message_type))

    




if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
