import requests
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