import requests
import json
from requests.auth import HTTPBasicAuth
ip = "http://18.189.117.13:2027"


def GetCooperateToken(cooperate = "kite test001", password = "85O17381U1"):# Get a token via a company for those without access
    tokenurl= "{}/cooperate/token".format(ip)
    responce = requests.get(tokenurl, auth=(cooperate, password))
    if responce.status_code == 200:
        token = responce.json()["body"]["token"]
        return token
    else:
        return responce.status_code

# print(GetCooperateToken())

def VerifyNumber(number):# Verify a number by getting a token
    verityurl = "{}/accounts/verifyNumber".format(ip)
    token =GetCooperateToken()
    try:
        bearer = "Bearer {}".format(token)       
        head = {'Authorization': bearer}
        responce = requests.post(verityurl, headers = head, json = number)
        return responce
    except Exception as e:
        print("failed to send otp")
        return "failed to send otp"
#  
# number = {"phoneNo":"254715232942"}
# responce  = VerifyNumber(number)
# print(responce)
# print(responce.text)




def CreateAccount(credentials, phoneNo, OTP):# Create an account by passing the phone Number, otp, password and username
    createAccounturl = "{}/accounts/consumer/register".format(ip)
    try:
        responce = requests.post(createAccounturl, auth=(phoneNo, OTP), json = credentials)
        return responce
    except Exception as e:
        return e


# credentials = {"username":"annonymax", "password":"password"}
# res = CreateAccount(credentials, phoneNo, OTP)

def GetUserToken(phoneNo, password):
    tokenUrl = "{}/accounts/login".format(ip)
    try:
        responce = requests.get(tokenUrl, auth=(phoneNo, password))
        return responce
    except:
        responce = {"status": "6"}
    return responce

# responce = GetUserToken("254715232942", "1234")
# print(responce)
# print(responce.json()["body"]["token"])
# print(responce.text)


# def GetUserData(phoneNo, password):
#     token = GetUserToken(phoneNo, password)
#     if token.status_code == 200:
#         print("continue")
#     else:
#         print("")
#     return token

def GetUserData(phoneNo, password):
    userInfoUrl = "{}/account".format(ip)
    token = GetUserToken(phoneNo, password)
    if token.status_code == 200:
        bearer = "Bearer {}".format(token.json()["body"]["token"])
        head = {'Authorization': bearer}
        response = requests.get(userInfoUrl, headers=head)
        return response
    else:
        return token

# responce = GetUserData("254715232942", "1234")
# print(responce)
# print(responce.text)


def GetAllTransactions(phoneNo, password):
    urlGetTransactions = "{}/transactions/walletActivities".format(ip)
    token = GetUserToken(phoneNo, password)
    if token.status_code == 200:
        bearer = "Bearer {}".format(token.json()["body"]["token"])
        head = {'Authorization': bearer}
        response = requests.get(urlGetTransactions, headers=head)
        return response
    else:
        print("Getting Transactions failed")

# res = GetAllTransactions("254715232942", "1234")
# print(res.text)
        



def WalletToWallet(phoneNo, password, data):
    wallet2walletUrl = "{}/transactions/walletToWallet".format(ip)
    token = GetUserToken(phoneNo, password)
    if token.status_code == 200:
        bearer = "Bearer {}".format(token.json()["body"]["token"])
        head = {'Authorization': bearer}
        response = requests.post(wallet2walletUrl, headers=head, json = data)
        return response
    else:
        return "token"

# reeee ={
#   "amount": 1,
#   "recipientNo": "001015232942"
# }
# responce = WalletToWallet("254715232942", "1234", reeee)
# print(responce)
# print(responce.text)

def MpesaToWallet(phoneNo, password, data):
    urlMpesaToWallet = "{}/transactions/mpesaToWallet".format(ip)
    token = GetUserToken(phoneNo, password)
    if token.status_code == 200:
        bearer = "Bearer {}".format(token.json()["body"]["token"])
        head = {'Authorization': bearer}
        response = requests.post(urlMpesaToWallet, headers=head, json = data)
        return response
    else:
        print("Mpesa to wallet failed")

    
# reeee = {
# 	"amount": 1,
# 	"phoneNo": "254715232942",
# 	"callBackUrl": "http://127.0.0.1:2027",
# 	"walletNo": "001015232942",
# 	"transactionDesc": "deposit to wallet"
# }
# res = MpesaToWallet("254715232942", "1234", reeee)
# print(res)
# print(res.text)


def CardToWallet(phoneNo, password, data):
    urlCardToWallet = "{}/transactions/cardToWallet".format(ip)
    token = GetUserToken(phoneNo, password)
    if token.status_code == 200:
        bearer = "Bearer {}".format(token.json()["body"]["token"])
        head = {'Authorization': bearer}
        response = requests.post(urlCardToWallet, headers=head, json = data)
        return response
    else:
        print("Mpesa to wallet failed")


# reeee = {
# 	  "cardNo": "4242424242424242",
# 	  "cvv": "812",
# 	  "expiryMonth": "01",
# 	  "expiryYear": "21",
# 	  "amount": 100,
# 	  "email": "max.sendeyo@kiteeholdings.biz",
# 	  "walletNo": "001015232942",
# 	  "callbackUrl": "http://18.189.117.13:2027"
# }
# responce = CardToWallet("254715232942", "1234", reeee)
# print(responce)
# print(responce.text)






###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

def Reqs():
    request = requests.get('http://18.189.117.13:2011/requests')
    data = request.json()
    return data


def GetToken(Username, Password):
    tokenUrl = 'http://18.189.117.13:2011/accounts/login'
    try:
        reply = requests.get(tokenUrl, auth=(Username, Password)).json()
    except:
        reply = {"status": "6"}
    return reply



# def GetUserData(Username, Password):
#     userInfoUrl = 'http://18.189.117.13:2011http://18.189.117.13:2027/cooperate/token/account'
#     token = GetToken(Username, Password)
#     response = ""
#     if eval(token["status"]) == 0:
#         bearer = "Bearer {}".format(token["data"]["token"])
#         head = {'Authorization': bearer}
#         response = requests.get(userInfoUrl, headers=head)
#     elif eval(token["status"]) == 6:
#         return response
#     else:
#         return response
#     return response




# email = '0715232942'
# password = 'pass1234'
# userdata = GetUserData(email, password)
# print(userdata.text)




def GetTransactions():
    urlGetTransactions = "http://18.189.117.13:2011/wallet/transactions/0010000000006"
    try:
        responce = requests.get(urlGetTransactions).json()
        print(responce[0])
    except:
        print("Serious error")

# print(GetTransactions())


def GetCoopToken(username, password):
    urlCoopToken = "http://18.189.117.13:2011/token"
    try:
        reply = requests.get(urlCoopToken, auth=(username, password)).json()
    except:
        reply = {"status": "6"}
    return reply





def DepositCard(data):
    urlDepositCard = "http://18.189.117.13:2011/thirdParties/cardPayment"
    token = GetCoopToken("Kite Holdings001", "xXcA1pGeBG")
    if eval(token["status"]) == 0:
        bearer = "Bearer {}".format(token["data"]["token"])       
        head = {'Authorization': bearer}
        response = requests.post(urlDepositCard, json = data, headers=head)
        return response
    try:
        print("funny")
    except:
        print("error")
    return response.json()




def DepositRequest(number, wallet, ammount):
    urlDepositRequest = "http://18.189.117.13:2011/thirdParties/mpesa/depositRequest"
    print("start")
    try:
        data = {
            "walletAccountNo": "{}".format(wallet),
            "phoneNo": "{}".format(number),
            "amount": ammount,
            "callBackUrl": "http://2ac713d5.ngrok.io/test",
            "referenceNumber": "{}".format(wallet),
            "transactionDesc": "transactionDesc"
        }
        responce = requests.post(urlDepositRequest, json = data)
        return responce
    except:
        print("passed")
        pass
    print("stop")

