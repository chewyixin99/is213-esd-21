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

    # if notificationBody['message_type'] == "order_notification":
    #     body = "\nHello User {}, your order {} is currently being processed. Details are as follows:\n".format(notificationBody["data"]["user_id"],notificationBody["data"]["order_id"])
    #     body += "\n--------------"
    #     body += "\nHawker ID: {}".format(notificationBody["data"]["hawker_id"])
    #     body += "\nItems: {}".format(notificationBody["data"]["items"])
    #     body += "\nTotal Price: ${}".format(notificationBody["data"]["total_price"])
    #     body += "\nDiscount: ${}".format(notificationBody["data"]["discount"])
    #     body += "\n\Final Price: ${}".format(notificationBody["data"]["final_price"])
    #     body += "\n--------------"
    #     body += "\nTime of Order: {}".format(notificationBody["data"]["time"])

    # elif notificationBody['message_type'] == "escrow_notification":
    #     body = "\nHello User {}, your payment {} to {} currently being processed. Details are as follows:\n".format(notificationBody["data"]["payer_id"],notificationBody["data"]["receiving_id"],notificationBody["data"]["order_id"])
    #     body += "\n--------------"
    #     body += "\n\Payment Amount: ${}".format(notificationBody["data"]["amount"])
    #     body += "\n--------------"
    #     body += "\nTime of Payment: {}".format(notificationBody["data"]["time"])
    
    client.messages.create(
        body=notificationBody,
        from_=twilio_number,
        to=target_number
    )
    print("Notification sent successfully..")

    




if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
