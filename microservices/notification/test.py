


body = "\n\n"
body += "\nHello User, your order is sent to the kitchen. \n\nDetails are as follows:"
body += "\n--------------"
body += "\nHawker ID: "
body += "\nItems: \n"

item_list = ['test','the']
for item in item_list:
    body += "- Item ID:, Qty: \n"
body += "--------------"
body += "\nTotal Price: $"
body += "\nDiscount: $"
body += "\nFinal Price: $"
body += "\n--------------"
body += "\nTime of Order:\nTue, 05 Apr 2022 01:31:12 GMT"

body2 = "\n"
body2 += "\nHello User , your order is completed.\n\nPayment details are as follows:"
body2 += "\n--------------"
body2 += "\nTotal Price: $"
body2 += "\nDiscount: $"
body2 += "\nFinal Price: $"
body2 += "\n--------------"
body2 += "\nTime of Order:\n "

print(body)
print(body2)