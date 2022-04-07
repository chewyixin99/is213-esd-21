import json
import os
from twilio.rest import Client
import amqp_setup

monitorBindingKey='*.notify'
account_sid = 'ACed3d23117c25da75a17a2c32b03f8fc7'
auth_token = 'c3cce512e7a30ce175024151ab3ab472'
twilio_number = '+15632073733'
target_number = '+6586862106'

def receiveOrderLog():
    amqp_setup.check_setup()
    print("Notification is received in notification.py")
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

    print("Received Body: {}".format(notificationBody))

    loaded_body = json.loads(notificationBody)
    
    # message_type = loaded_body['message_type']
    data = loaded_body["data"]
    body = ""

    print("Message Type: {} is received".format(loaded_body["message_type"]))

    if loaded_body["message_type"] == "order_notification":

        body = "\n\n"
        body += "\nHello User {}, your order {} is sent to the kitchen. \n\nDetails are as follows:".format(data["user_id"],data["order_id"])
        body += "\n--------------"
        body += "\nHawker ID: {}".format(data["hawker_id"])
        body += "\nItems: \n"

        item_list = eval(data["items"])
        for item in item_list:
            body += "- Item ID: {}, Qty: {}\n".format(item["item_id"],item["quantity"])
        body += "--------------"
        body += "\nTotal Price: ${}".format(data["total_price"])
        body += "\nDiscount: ${}".format(data["discount"])
        body += "\nFinal Price: ${}".format(data["final_price"])
        body += "\n--------------"
        body += "\nTime of Order:\n{}".format(data["time"])

        # print("Notification: {} sent successfully..".format(message_type))
        

    elif loaded_body["message_type"] == "accept_notification":
        body = "\n"
        body += "\nHello User {}, your order {} is being processed.".format(data["user_id"],data["order_id"])
        body += "\n\n--------------"
        body += "\nEstimated Waiting Time: 20mins"

        # print("Notification: {} sent successfully..".format(message_type))


    elif loaded_body["message_type"] == "order_completion_notification":
        body = "\n"
        body += "\nHello User {}, your order {} is completed.\n\nPayment details are as follows:".format(data["user_id"],data["order_id"])
        body += "\n--------------"
        body += "\nTotal Price: ${}".format(data["total_price"])
        body += "\nDiscount: ${}".format(data["discount"])
        body += "\nFinal Price: ${}".format(data["final_price"])
        body += "\n--------------"
        body += "\nTime of Order:\n{}".format(data["time"])

        # print("Notification: {} sent successfully..".format(message_type))

    elif loaded_body["message_type"] == "reject_notification":
        body = "\n"
        body += "\nHello User {}, your order {} was rejected.".format(data["user_id"],data["order_id"])
        body += "\n\n--------------"
        body += "\nPlease try again later.."

    if body != "":
        client.messages.create(
            body=body,
            from_=twilio_number,
            to=target_number
        )
        
        print("Notification was sent successfully..")

    




if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
