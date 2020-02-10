from flask import Flask, render_template, request, url_for, redirect, session
import os, time
from passlib.hash import sha256_crypt
import csvs
import apis
# from werkzeug.utils import secure_filenames
import data
import fun
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.urandom(24)


app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='anonymaxdashone@gmail.com',
    MAIL_PASSWORD='17571757'
)
mail = Mail(app)

######################################################

def determineType_function(operation):
    if operation == "send":
        return "Sent to "
    elif operation == "receive":
        return "Recieved from "

def make_it_money(value):
    value = 'Ksh {:,.2f}'.format(value)
    return value
    
def transaction_date_format(date):
    convertedDate = fun.Convert4User(date)
    return convertedDate
    
def admin_date_format(date):
    convertedDate = fun.Convert4Admin(date)
    return convertedDate


app.jinja_env.globals.update(determineType_function=determineType_function)
app.jinja_env.globals.update(make_it_money=make_it_money)
app.jinja_env.globals.update(transaction_date_format=transaction_date_format)
app.jinja_env.globals.update(admin_date_format=admin_date_format)



######################################################

@app.errorhandler(404)
def Page_not_found(e):
    return render_template("/404.html", error=e, message="Sorry, Page was not found")


@app.errorhandler(400)
def BadRequest(e):
    return render_template("/404.html",  error=e, message="Sorry, Bad Request")


@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

def UpdateUserData():
    response = apis.GetUserData(session["phoneNumber"], session["password"])
    userdata = response.json()
    userdata = userdata["body"]
    userdata["admins"] = ["254715232942","254797162465","254792383998","254722774403"]
    session["userdata"] = userdata

@app.route("/", methods=["GET", "POST"])
def Login():
    if "userdata" in session:
        return redirect("/home")
    else:
        if request.method == "POST":
            phoneNo = request.form["phoneNumber"]
            phoneNumber ="254{}".format(phoneNo[-9:])
            password = request.form["password"]
            try:
                responce = apis.GetUserData(phoneNumber, password)
                if responce.status_code == 200:
                    session["phoneNumber"] = phoneNumber
                    session["password"] = password
                    userdata = responce.json()
                    userdata = userdata["body"]
                    userdata["admins"] = ["254715232942","254797162465","254792383998","254722774403","254704187447"]
                    session["userdata"] = userdata
                    print(session["userdata"])
                    time.sleep(1)
                    return redirect("/")
                else:
                    error = "PLEASE CHECK YOUR CREDENTIALS"
                    return render_template("/kite/login.html", error=error)
            except:
                error = "Server error"
                return render_template("/kite/login.html", error=error)
        else:
            return render_template("/kite/login.html")
    return render_template("/kite/login.html")


@app.route("/register", methods=["GET", "POST"])
def Register():
    if request.method == "POST":
        phoneNumber = request.form["phoneNumber"]
        if len(phoneNumber) < 9:
            error = "Phone Number too short"
            return render_template("kite/getOtp.html", error = error)
        elif len(phoneNumber) > 10:
            error = "Phone Number should be at most 10 characters"
            return render_template("kite/getOtp.html", error = error)
        elif phoneNumber[:2] == "07" or phoneNumber[:1] == "7":
            phoneNumber ="254{}".format(phoneNumber[-9:])
            if len(phoneNumber) > 12:
                error = "Phone Number should be at most 10 characters"
                return render_template("kite/getOtp.html", error = error)
            number = {"phoneNo":phoneNumber}
            responce = apis.VerifyNumber(number)
            if responce.status_code == 200:
                session["phoneNo"]= phoneNumber
                time.sleep(1)
                return redirect("/passwordVerification")
            else:
                error ="Sorry! Please try again."
                return render_template("kite/getOtp.html", error = error)
        else:
            error = "Please use a right number"
            return render_template("kite/getOtp.html", error = error)
    return render_template("kite/getOtp.html")


@app.route("/passwordVerification", methods=["GET", "POST"])
def PassVerification():
    if request.method == "POST":
        username = request.form["username"]
        otp = request.form["OTP"]
        password = request.form["password"]
        confirm = request.form["cpassword"]
        if password != confirm:
            return render_template("/kite/setPassword.html", error="Password missmatch")
        else:
            credentials = {"username":username, "password":password}
            try:
                res = apis.CreateAccount(credentials ,session["phoneNo"], otp)
                if res.status_code == 200:
                    return redirect("/")
                else:
                    return render_template("/kite/setPassword.html", message=res.text)
            except Exception as e:
                print(e)
                return render_template("/kite/setPassword.html", error="Verification failed Try again")
            
    else:
        message = "Please Use the Otp sent to your phone"
        return render_template("/kite/setPassword.html", message=message)


tiles = [
    {"name": "My Account", "icon": "fas fa-fw fa-user", "color": "bg-primary"},
    {"name": "Top Up", "icon": "fas fa-fw fa-wallet", "color": "bg-warning"},
    {"name": "Send to Wallet", "icon": "fas fa-fw fa-paper-plane", "color": "mainColor"},

    {"name": "Send to Bank", "icon": "fas fa-fw fa-paper-plane", "color": "subColor"},
    
    {"name": "Send to Mpesa", "icon": "fas fa-fw fa-paper-plane", "color": "bg-success"},
    {"name": "Billers", "icon": "fas fa-fw fa-money-bill-wave", "color": "bg-info"},
    
    # {"name": "Admin Panel", "icon": "fas fa-fw fa-toolbox", "color": "bg-danger"},
]
@app.route("/home")
def Home():
    if "userdata" in session:
        return render_template("kite/home.html", tiles=tiles, userdata=session["userdata"])
    else:
        return redirect("/")


@app.route("/home/<string:tile>", methods=["GET", "POST"])
def Tiles(tile):
    if tile == "My Account":
        return redirect("/profile")
    elif tile == "Send to Wallet":
        return redirect("/sendToWallet")
    elif tile == "Send to Bank":
        return redirect("/sendToBank")
    elif tile == "Send to Mpesa":
        return redirect("/sendToMpesa")
    elif tile == "Top Up":
        return redirect("/Top Up")
    elif tile == "Admin Panel":
        return redirect("/Dashboard")
    elif tile == "Billers":
        return redirect("/Billers")
    else:
        return "{}".format(tile)



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
@app.route("/Billers", methods = ["POST", "GET"])
def Billers():
    if "userdata" in session:
        if request.method == "POST":
            if request.form["purpose"] == "validate":
                account = request.form["account"]
                serviceID = request.form["serviceID"]
                data = {
                        "serviceID": serviceID,
                        "accountNumber": "{}".format(account)
                        }
                try:
                    responce = apis.CellulantValidation(data)
                    if isinstance(responce.status_code, int):
                        print(responce)
                        print(responce.text)
                        message = responce.json()["body"]
                        if responce.status_code == 200:
                            return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, message = message)
                        return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, warning = message)
                    else:
                        message = responce
                        return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, error = message)
                except Exception as e:
                    error = e
                    return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, error = error)
            elif request.form["purpose"] == "query":
                account = request.form["account"]
                serviceID = request.form["serviceID"]
                data = {
                        "serviceID": serviceID,
                        "accountNumber": "{}".format(account)
                        }
                try:
                    responce = apis.CellulantQuerying(data)
                    if isinstance(responce.status_code, int):
                        print(responce)
                        print(responce.text)
                        message = responce.json()["body"]
                        if responce.status_code == 200:
                            return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, message = message)
                        return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, warning = message)
                    else:
                        message = responce
                        return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, error = message)
                except Exception as e:
                    error = e
                    return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, error = error)
            elif request.form["purpose"] == "paybill":
                account = request.form["account"]
                serviceID = request.form["serviceID"]
                amount = request.form["amount"]
                data = {
                        "serviceID": serviceID,
                        "accountNumber": "{}".format(account),
                        "amount": "{}".format(amount)
                        }
                try:
                    responce = apis.CellulantPayment(data)
                    if isinstance(responce.status_code, int):
                        print(responce)
                        print(responce.text)
                        message = responce.json()["body"]
                        if responce.status_code == 200:
                            return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, message = message)
                        return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, warning = message)
                    else:
                        message = responce
                        return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, error = message)
                except Exception as e:
                    error = e
                    return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers, error = error)
        return render_template("/kite/billers.html", userdata = session["userdata"], billers = billers)
    return redirect("/")







@app.route("/profile")
def Profile():
    if "userdata" in session:
        UpdateUserData()
        transactions = apis.GetAllTransactions(session["phoneNumber"], session["password"])
        if transactions.status_code == 200:
            transactions = transactions.json()["body"]
            return render_template("/kite/profile.html", userdata=session["userdata"], transactions = transactions)
        else:
            transactions = []
            return render_template("/kite/profile.html", userdata=session["userdata"], transactions = transactions)
        
    else:
        return redirect("/")

@app.route("/demo")
def Demo():
    return render_template("/kite/del.html",  userdata=session["userdata"])

@app.route("/sendToBank", methods = ["GET","POST"])
def SendToBank():
    if "userdata" in session:
        banks = apis.GetBankNames()
        if request.method == "POST":
            bankName = request.form["bankName"]
            recipientNo = request.form["credit-card"]
            amount = request.form["amount"]
            amount = amount.replace("Ksh ","")
            recipientNo = recipientNo.replace(" - ","")
            print(amount)
            print(recipientNo)
            try:
                if eval(amount) < 5:# or eval(amount) > 50000:
                    error = "You cant send less than ksh 5.00"
                    return render_template("/kite/sendToBank.html", userdata = session["userdata"], banks = banks, error=error)                                    
                elif eval(amount) > 50000:
                    error = "You cant send More than ksh 50,000.00"
                    return render_template("/kite/sendToBank.html", userdata = session["userdata"], banks = banks, error=error)                
                else:
                    error = "Congrats test success"
                    return render_template("/kite/sendToBank.html", userdata = session["userdata"], banks = banks, error=error)
            except Exception as e:
                error = e
                return render_template("/kite/sendToBank.html", userdata = session["userdata"], banks = banks, error=error)
            data = {
                        "accountNumber": amount,
                        "bankCode": banks[bankName],
                        "amount": amount,
                        "transactionCurrency": "KES",
                        "narration": "Money transfer from Kite Wallet"
                    }
        else:
            return render_template("/kite/sendToBank.html", userdata = session["userdata"], banks = banks)
    else:
        return redirect("/")

@app.route("/sendToWallet", methods = ["GET", "POST"])
def SendToWallet():
    if "userdata" in session:
        if request.method == "POST":
            account = request.form["accountNo"]
            amount = request.form["amount"]
            amount = amount.replace("Ksh ","")

            if eval(amount) < 5:
                error = "You cant Transact less than ksh 5.00"
                return render_template("/kite/sendToWallet.html", userdata = session["userdata"], error = error)
            elif eval(amount) > 50000:
                error = "You cant Transact More than ksh 50000.00"
                return render_template("/kite/sendToWallet.html", userdata = session["userdata"], error = error)
            else:
                data ={
                "amount": amount,
                "recipientNo": "0010{}".format(account[-8:])
                }
                responce = apis.WalletToWallet(session["phoneNumber"], session["password"], data)
                if responce.status_code == 200:
                    message = " Ksh {} sent to {}". format(amount, account)
                    return render_template("/kite/sendToWallet.html", userdata = session["userdata"], message = message)
                else:
                    error = responce.text
                    return render_template("/kite/sendToWallet.html", userdata = session["userdata"], notification = error)
        else:
            pass
        return render_template("/kite/sendToWallet.html", userdata = session["userdata"])
    else:
        return redirect("/")


@app.route("/sendToMpesa", methods = ["GET", "POST"])
def SendToMpesa():
    if "userdata" in session:
        if request.method == "POST":
            account = request.form["accountNo"]
            amount = request.form["amount"]
            amount = amount.replace("Ksh ","")

            if eval(amount) < 5:
                error = "You cant Transact less than ksh 5.00"
                return render_template("/kite/sendToMpesa.html", userdata = session["userdata"], error = error)
            elif eval(amount) > 50000:
                error = "You cant Transact More than ksh 50000.00"
                return render_template("/kite/sendToMpesa.html", userdata = session["userdata"], error = error)
            else:
                error = "The test works, feature coming soon"
                return render_template("/kite/sendToMpesa.html", userdata = session["userdata"], notification = error)

                # data ={
                # "amount": amount,
                # "recipientNo": "0010{}".format(account[-8:])
                # }
                # responce = apis.WalletToWallet(session["phoneNumber"], session["password"], data)
                # if responce.status_code == 200:
                #     message = "Sending Ksh {} to {} Scuccessful". format(amount, account)
                #     return render_template("/kite/sendToMpesa.html", userdata = session["userdata"], message = message)
                # else:
                #     error = responce.text
                #     return render_template("/kite/sendToMpesa.html", userdata = session["userdata"], notification = error)
        else:
            pass
        return render_template("/kite/sendToMpesa.html", userdata = session["userdata"])
    else:
        return redirect("/")


@app.route("/Top Up", methods=["GET", "POST"])
def ChooseMethod():
    if "userdata" in session:
        try:
            if request.method == "POST":
                if request.form["paymentMethod"] == "mpesa":
                    print("mpesa means")
                    number = request.form["phoneNo"]
                    wallet = request.form["walletNo"]
                    amount = request.form["amount"]
                    amount = amount.replace("Ksh ","")
                    data = {
                            	"amount": amount,
                            	"phoneNo": "254{}".format(number[-9:]),
                            	"callBackUrl": apis.ip,
                            	"walletNo": "0010{}".format(wallet[-8:]),
                            	"transactionDesc": "deposit to wallet"
                            }
                    responce = apis.MpesaToWallet(session["phoneNumber"], session["password"], data)
                    res = responce.json()
                    if responce.status_code == 200:
                        message = "Check phone holding number {} to complete transaction.".format(
                            number)
                        return render_template("/kite/chooseMethod.html", userdata=session["userdata"], message=message)
                    elif responce.status_code == 500:
                        message = "Please wait for a while. Another Transaction is pending"
                        return render_template("/kite/chooseMethod.html", userdata=session["userdata"], warning=message)
                    elif responce.status_code == 400:
                        message = res["errorMessage"]
                        return render_template("/kite/chooseMethod.html", userdata=session["userdata"], error=message)

                elif request.form["paymentMethod"] == "card":
                    print("card means")
                    cardNo = request.form["cardNo"]
                    cvv = request.form["cvv"]
                    month = request.form["month"]
                    year = request.form["year"]
                    walletNo = request.form["walletNo"]
                    amount = request.form["amount"]
                    email = request.form["email"]
                    cardNo = cardNo.replace(" - ", "")
                    amount = amount.replace("Ksh ","")
                    amount = amount.replace(",","")
                    if eval(amount) > 50000:
                        error = "Sorry cant send more than ksh 50000"
                        return render_template("/kite/chooseMethod.html", userdata=session["userdata"], error = error)
                    reeee = {
                    	  "cardNo": cardNo,
                    	  "cvv": cvv,
                    	  "expiryMonth": month,
                    	  "expiryYear": year,
                    	  "amount": amount,
                    	  "email": email,
                    	  "walletNo": "0010{}".format(walletNo[-8:]),
                    	  "callbackUrl": apis.ip
                    }
                    print(reeee)
                    try:
                        responce = apis.CardToWallet(session["phoneNumber"], session["password"], reeee).json()
                        return redirect(responce["body"]["data"]["authurl"])
                    except Exception as e:
                        error = "Sorry an error occured"
                        return render_template("/kite/chooseMethod.html", userdata=session["userdata"], error = error)
                else:
                    print("unspecified method")

            else:
                return render_template("/kite/chooseMethod.html", userdata=session["userdata"])
        except:
            return render_template("/kite/chooseMethod.html", userdata=session["userdata"], error = "Sorry Process failed")

    else:
        return redirect("/")
# #############################################################################################
# ##########/#\##########|#\#####/#|#####|#####################################################
# #########/###\#########|##\###/##|#####|#####################################################
# ########/#####\########|###\#/###|#####|#####################################################
# #######/-------\#######|#########|#####|#####################################################
# ######/#########\######|#########|#####|#####################################################
# #####/###########\#####|#########|#####|#####################################################
# #############################################################################################



@app.route("/adminLogin", methods = ["GET", "POST"])
def AdminLogin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print(email, password)
        if email == password:
            if email == "admin@email.com":
                session["administrator"] = email
                return redirect("/Dashboard")
    return render_template("adminPages/adminLogin.html")





@app.route("/Dashboard/")
def Dashboard():
    if "userdata" in session:
        if session["userdata"]["phoneNo"] in session["userdata"]["admins"]:
            session["administrator"] = session["userdata"]
            reqs = Numbers(data.DashData())
            balance = apis.GetCoopBalance()
            return render_template("/adminPages/dashboard.html", dashboard="active", cardsData=reqs, balance= balance)
        else:
            print("Userdata error login")      
    else:
        return redirect("/")

################################## Admin functions ########################
################################## Admin functions ########################

@app.route("/Dashboard/Admin", methods = ["GET", "POST"])
def Administrator():
    if "administrator" in session:
        if request.method == "POST":
            if request.form["formName"] == "createMerchant":
                cooperateCode = request.form["code"]
                companyName = request.form["companyName"]
                username = request.form["username"]
                phoneNo = request.form["phoneNo"]
                data = {
                "username": username,
                "companyName": companyName,
                "cooprateCode": cooperateCode,
                "phoneNo": phoneNo
                }
                try:
                    responce = apis.RegisterMerchant(data)

                    if responce.status_code == 200:
                        message = "Status {}: {}".format(responce.status_code, responce.json()["body"])
                        return render_template("/adminPages/admin.html", admin = "active", message = message)
                    else:
                        error = "error {}: {}".format(responce.status_code, responce.json()["body"])
                        return render_template("/adminPages/admin.html", admin = "active", error = error)
                except Exception as e:
                    pass


        return render_template("/adminPages/admin.html", admin = "active")
    else:
        return redirect("/adminLogin")
        
        
@app.route("/Dashboard/Merchants")
def Merchants():
    if "administrator" in session:
        logs = apis.GetMerchant()
        if logs.status_code == 200:
            print("showing merchant")
            return render_template("/adminPages/config/merchants.html", admin = "active", logs = logs.json()) 
        else:
            print("failed   hhhhh")
            error = apis.GetMerchant()
            return "an error occured"

    else:
        return redirect("/adminLogin")







################################## Admin functions ########################
################################## Admin functions ########################


################################## bird logs ########################
################################## bird logs ########################
@app.route("/kitebird/otps")
def OTPS():
    if "administrator" in session:
        logs = apis.BirdAllOtps()
        return render_template("/adminPages/kitebird/otps.html" , kitebird = "active", logs = logs)
    return redirect("/adminLogin")

    

@app.route("/kitebird/accountCreation")
def AccountCreation():
    logs = apis.BirdAccounts()
    return render_template("/adminPages/kitebird/accountCreation.html" , kitebird = "active", logs = logs)


@app.route("/kitebird/accountLogins")
def WalletLogins():
    logs = apis.BirdLogins()
    return render_template("/adminPages/kitebird/accountLogins.html" , kitebird = "active", logs = logs)


@app.route("/kitebird/unusedOtps")
def UnusedOtps():
    logs = apis.BirdMpesaWallet()
    return render_template("/adminPages/kitebird/unusedOtps.html" , kitebird = "active", logs = logs)



@app.route("/kitebird/errorResponses")
def ErrorResponses():
    logs = apis.BirdErrors()
    return render_template("/adminPages/kitebird/errorResponses.html" , kitebird = "active", logs = logs)


@app.route("/kitebird/fewResponses")
def FewResponses():
    logs = apis.BirdResponces()
    return render_template("/adminPages/kitebird/fewResponses.html" , kitebird = "active", logs = logs)


@app.route("/kitebird/fewRequests")
def FewRequests():
    logs = apis.BirdRequests()
    return render_template("/adminPages/kitebird/fewRequests.html" , kitebird = "active", logs = logs)


@app.route("/kitebird/walletToWallet")
def WalletToWallet():
    logs = apis.BirdWalletWallet()
    return render_template("/adminPages/kitebird/walletToWallet.html" , kitebird = "active", logs = logs)


@app.route("/kitebird/cardToWallet")
def CardToWallet():
    logs = apis.BirdCardWallet()
    return render_template("/adminPages/kitebird/cardToWallet.html" , kitebird = "active", logs = logs)


@app.route("/kitebird/mpesaToWallet")
def MpesaToWallet():
    logs = apis.BirdMpesaWallet()
    return render_template("/adminPages/kitebird/walletToWallet.html" , kitebird = "active", logs = logs)
    




################################## bird logs ########################
################################## bird logs ########################
################################## bird logs ########################
################################## bird logs ########################


reses = []
@app.route("/tables/<string:name>")
def Tables(name):
    if name == "mpesa":
        reses = data.Responses()
        mpesaLogs = data.MpesaLogs()
        return render_template("/adminPages/tables/mpesaTable.html", tables="active", mpesaLogs=mpesaLogs)
    elif name == "card":
        mpesaLogs = data.CardLogs()
        return render_template("/adminPages/tables/cardTable.html", tables="active", mpesaLogs=mpesaLogs)
    elif name == "token":
        mpesaLogs = data.TokenLogs()
        return render_template("/adminPages/tables/tokenTable.html", tables="active", mpesaLogs=mpesaLogs)


def responceState(id):
    return "{} pppp".format(id)


app.jinja_env.globals.update(responceState=responceState)


@app.route("/charts/")
def Charts():
    return render_template("/adminPages/charts.html", charts="active")


@app.route("/admin")
def Admin():
    if "administrator" in session:
        tableData = ["Logs Table"]
        tableData.append(data.DashData())
        reqs = Numbers(data.DashData())

        return render_template("/adminPages/dashboard.html", logs=tableData, cardsData=reqs)
    else:
        return redirect("/adminLogin")


@app.route("/upload/<string:value>", methods=["GET", "POST"])
def Upload(value):
    if "username" in session:
        path = "static/uploads"
        uploads = csvs.GetFiles(path)
        if value == "upload":
            file = request.files["file"]
            filename = file.filename
            file.save(os.path.join(path, filename))
            uploads = csvs.GetFiles(path)
            return render_template("/adminPages/uploads.html", message="File uploaded", uploads=uploads)

        elif value in uploads:
            try:
                content = csvs.Read(value, path)
            except:
                content = [["This file is not a csv file"],
                           ["This file is not a csv file"]]

            return render_template("/adminPages/uploads.html", content=content, uploads=uploads)

        elif value == "delete":
            return render_template("/adminPages/uploads.html", warning="File Deleted", uploads=uploads)

        else:
            return render_template("/adminPages/uploads.html", uploads=uploads)

    else:
        return redirect("/")


def send_mail(email, subject, message):
    try:
        msg = Message("My Test Emails!",
                      sender="anonymaxdashone@gmail.com",
                      recipients=[email])
        msg.body = message
        mail.send(msg)
        return 'Mail sent!'
    except Exception as e:
        return(str(e))


@app.route("/emailSender", methods=["GET", "POST"])
def EmailSender():
    if request.method == "POST":
        to = request.form["recipient"]
        subject = request.form["subject"]
        email = request.form["email"]
        # em = "{}  {}  {}".format(to, subject, email)
        send_mail(to, subject, email)
    return render_template("/editor.html")


@app.route("/fake")
def Fake():
    return render_template("home.html", tiles=tiles)


@app.route("/kite")
def Kite():
    # rows = data.DashData()
    rows = []
    return render_template("/kite/home.html", rows=rows)


@app.route("/upload/<string:action>/<string:value>")
def UploadActions(action, value):
    if action == "delete":
        info = csvs.Delete("static/uploads", value)
        uploads = csvs.GetFiles("static/uploads")
        return redirect("/upload/delete")


@app.route("/trial")
def Trial():
    return render_template("adminPages/trial.html")


@app.route("/compute/<string:action>/<string:name>")
def ComputeCSV():
    uploads = csvs.GetFiles("static/uploads")
    return render_template("/adminPages/compute.html", uploads=uploads)


@app.route("/compute/<string:name>")
def Compute(name):
    uploads = csvs.GetFiles("static/uploads")
    return render_template("/adminPages/compute.html", uploads=uploads)


@app.route("/sync")
def Sync():
    return render_template("/adminPages/sync.html")


def Numbers(req):
    reqs = {}
    reqs.update({"allreq": len(req)})
    x = 0
    y = 0
    for logs in req:
        if logs["requestType"] == "mpesaStkPush":
            x += 1
        elif logs["requestType"] == "card":
            y += 1
        else:
            pass
    reqs.update({"mpesareq": x})
    reqs.update({"cardreq": y})
    return reqs

determineType_function
def clever_function(date):
    convertedDate = fun.Convert(date)
    return convertedDate


app.jinja_env.globals.update(clever_function=clever_function)


@app.route("/forgot-password")
def ForgotPassword():
    return render_template("/kite/forgot-password.html")


if __name__ == "__main__":
    app.run(debug=True)
