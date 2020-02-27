import requests

#Hardcoded administrators
administrators = ["254715232942","254797162465","254792383998","254722774403"]

### Home page tiles data
tiles = [
    {"name": "My Account", "icon": "fas fa-fw fa-user", "color": "bg-primary"},
    {"name": "Top Up", "icon": "fas fa-fw fa-wallet", "color": "bg-warning"},
    {"name": "Send to Wallet", "icon": "fas fa-fw fa-paper-plane", "color": "mainColor"},
    {"name": "Send to Bank", "icon": "fas fa-fw fa-paper-plane", "color": "subColor"},
    {"name": "Send to Mpesa", "icon": "fas fa-fw fa-paper-plane", "color": "bg-success"},
    {"name": "Billers", "icon": "fas fa-fw fa-money-bill-wave", "color": "bg-info"},
    # {"name": "Admin Panel", "icon": "fas fa-fw fa-toolbox", "color": "bg-danger"},
]


#billers data
billers = [
    {"serviceId":"1", "name": "DSTV", "Description":"Subscription on", "image": "/static/images/DStvlogo.png", "color": "bg-primary"},
    {"serviceId":"2", "name": "GOTV", "Description":"Subscription on", "image": "/static/images/GOtv.jpg", "color": "mainColor"},
    {"serviceId":"441", "name": "Startimes", "Description":"Subscription on", "image": "/static/images/startimes.jpg", "color": "subColor"},
    {"serviceId":"717", "name": "KWESE", "Description":"Subscription on", "image": "/static/images/Kwese.jpg", "color": "bg-info"},
    {"serviceId":"43", "name": "ZUKU", "Description":"Subscription on", "image": "/static/images/Zuku-logo.jpg", "color": "bg-info"},
    {"serviceId":"9", "name": "Safaricom", "Description":"Airtme top up on", "image": "/static/images/mpesa.png", "color": "bg-success"},
    {"serviceId":"54", "name": "Airtel", "Description":"Airtme top up on", "image": "/static/images/airtel.png", "color": "bg-danger"},
    {"serviceId":"55", "name": "TelKom", "Description":"Airtme top up on", "image": "/static/images/telkom.jpg", "color": "mainColor"},
    {"serviceId":"378", "name": "KPLC-Postpay", "Description":"Electricity", "image": "/static/images/kplc.jpg", "color": "bg-primary"},
    {"serviceId":"337", "name": "KPLC-Prepaid", "Description":"Electricity", "image": "/static/images/kplc.jpg", "color": "bg-primary"},
    {"serviceId":"8", "name": "Jambojet", "Description":"Ticket", "image": "/static/images/", "color": "subColor"},
    {"serviceId":"000", "name": "Nairobi-Water", "Description":"", "image": "/static/images/nairobi.png", "color": "bg-info"},
]


##All banks supported
banklist = {"KCB":1, 2:"Standard Charteed Bank KE", "Barclays Bank":3, "CBA":7, "Prime Bank":10,
    "Cooperative Bank":11, "National Bank":12, "Citibank":16, "Habib Bank AG Zurich":17, "Middle East Bank":18,
    "Bank of Africa":19, "Consolidated Bank":23, "Credit Bank Ltd":25, "Stanbic Bank":31, "ABC bank":35, "NIC Bank":41,
    "Spire Bank":49, "Paramount Universal Bank":50, "Jamii Bora Bank":51, "Guaranty Bank":53, "Victorial Commercial Bank":54,
    "Guardian Bank":55, "I&M Bank":57, "DTB":63,
    "Sidian Bank":66, "Equity Bank":68, "Family Bank":70, "Gulf African Bank":72, "First Community Bank":74, "KWFT Bank":78
    }

#### Kite cooperate token and password

cooperate = {
    "name":"kite test001",
    "password":"85O17381U1"
}





######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
ip = "http://18.189.117.13:2011"
# def DashData():
#     request = requests.get('http://18.189.117.13:2011/requestM')
#     data = request.json()
#     return data


def Responces():
    request = requests.get('http://18.189.117.13:2011/responses')
    data = request.json()
    return data



# def ErrorResponses():
#     errors = []
#     data = Responces()
#     for row in data:
#         newData = (row["responseBody"])
#         try:
#             if newData["errorMessage"]:
#                 errors.append(row)
#             else:
#                 pass
#         except:
#             pass
#     return errors

def DashData():
    request = requests.get('http://18.189.117.13:2011/requests')
    data = request.json()
    return data

def Requests():
    request = requests.get('http://18.189.117.13:2011/requests')
    data = request.json()
    return data

def Responses():
    request = requests.get('http://18.189.117.13:2011/responses')
    data = request.json()
    return data

def ErrorResponses():
    errors = []
    data = Responces()
    for row in data:
        newData = (row["responseBody"])
        try:
            if newData["errorMessage"]:
                errors.append(row)
            else:
                pass
        except:
            pass
    return errors

card = []

def MpesaLogs():
    mpesa = []
    req = Requests()
    # res = Responses()
    for request in req:
        if request["requestType"] == "mpesaStkPush":
            mpesa.append(request)
    return mpesa

def CardLogs():
    mpesa = []
    req = Requests()
    # res = Responses()
    for request in req:
        if request["requestType"] == "card":
            mpesa.append(request)
    return mpesa


def TokenLogs():
    mpesa = []
    req = Requests()
    # res = Responses()
    for request in req:
        if request["requestType"] == "token":
            mpesa.append(request)
    return mpesa


# reses = Responses()
# def CheckRes():
#     names = [{"name":"him", "color":"grey"},{"name":"max", "color":"black"},{"name":"you", "color":"yellow"},{"name":"me", "color":"green"}]
#     if any(d['requestId'] == '5dcc2e66d4346d11c4116c9c' for d in reses):
#         return "true"
#     else:
#         return "false"



# print(CheckRes())