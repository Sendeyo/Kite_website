from flask import Flask, render_template, request, url_for, redirect, session
import os
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
    session["userdata"] = userdata["body"]

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
                    session["userdata"] = userdata["body"]
                    print(session["userdata"])
                    return redirect("/home")
                else:
                    error = "PLEASE CHECK YOUR CREDENTIALS"
                    return render_template("/kite/login.html", error=error)
            except:
                error = "Server error"
                print(error)
                return render_template("/kite/login.html", error=error)
        else:
            return render_template("/kite/login.html")


@app.route("/register", methods=["GET", "POST"])
def Register():
    if request.method == "POST":
        phoneNumber = request.form["phoneNumber"]
        phoneNumber ="254{}".format(phoneNumber[-9:])
        print(phoneNumber)
        number = {"phoneNo":phoneNumber}
        res = apis.VerifyNumber(number)
        if res.status_code == 200:
            session["phoneNo"] = phoneNumber
            return redirect("/passwordVerification")
        else:
            error = res.text
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
            credentials = {"username":"", "password":password}
            res = apis.CreateAccount(credentials ,session["phoneNo"], otp)
            if res.status_code == 200:
                return render_template("/kite/login.html", message="You can now login")
            else:
                return render_template("/kite/setPassword.html", message=res.text)
    else:
        message = "Please Use the Otp sent to your phone"
        return render_template("/kite/setPassword.html", message=message)


tiles = [
    {"name": "My Account", "icon": "fas fa-fw fa-user", "color": "bg-primary"},
    {"name": "Send to Wallet", "icon": "fas fa-fw fa-paper-plane", "color": "mainColor"},
    {"name": "Top Up", "icon": "fas fa-fw fa-wallet", "color": "bg-warning"},
    {"name": "Send to Mpesa", "icon": "fas fa-fw fa-paper-plane", "color": "bg-success"},
    {"name": "Billers", "icon": "fas fa-fw fa-money-bill-wave", "color": "bg-info"},
    
    {"name": "Admin Panel", "icon": "fas fa-fw fa-toolbox", "color": "bg-danger"},
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
    elif tile == "Top Up":
        return redirect("/Top Up")
    elif tile == "Admin Panel":
        return redirect("/Dashboard")
    else:
        return "{}".format(tile)


@app.route("/profile")
def Profile():
    if "userdata" in session:
        UpdateUserData()
        return render_template("/kite/profile.html", userdata=session["userdata"])
    else:
        return redirect("/")


@app.route("/sendToWallet", methods = ["GET", "POST"])
def SendToWallet():
    if "userdata" in session:
        if request.method == "POST":
            account = request.form["accountNo"]
            amount = request.form["amount"]
            return render_template("/kite/sendToWallet.html", userdata = session["userdata"], notification = "That was successful")
        else:
            pass
        return render_template("/kite/sendToWallet.html", userdata = session["userdata"])
    else:
        return redirect("/")

@app.route("/Top Up", methods=["GET", "POST"])
def ChooseMethod():
    if "userdata" in session:
        try:
            if request.method == "POST":
                if request.form["paymentMethod"] == "mpesa":
                    number = request.form["phoneNo"]
                    wallet = request.form["walletNo"]
                    amount = request.form["amount"]
                    responce = apis.DepositRequest(number, wallet, amount)
                    res = responce.json()
                    if responce.status_code == 200:
                        message = "Check phone holding Number {} to complete transaction".format(
                            number)
                        return render_template("/kite/chooseMethod.html", userdata=session["userdata"], message=message)
                    elif responce.status_code == 500:
                        message = "Please wait for a while. Another Transaction is pending"
                        return render_template("/kite/chooseMethod.html", userdata=session["userdata"], warning=message)
                    elif responce.status_code == 400:
                        message = res["errorMessage"]
                        return render_template("/kite/chooseMethod.html", userdata=session["userdata"], error=message)
                elif request.form["paymentMethod"] == "card":
                    cardNo = request.form["cardNo"]
                    cvv = request.form["cvv"]
                    walletNo = request.form["walletNo"]
                    amount = request.form["amount"]
                    email = request.form["email"]
                    data = {
                        "cardNo": "{}".format(cardNo),
                        "cvv": "{}".format(cvv),
                        "expiryMonth": "01",
                        "expiryYear": "21",
                        "currency": "KES",
                        "country": "KE",
                        "amount": "{}".format(amount),
                        "email": "{}".format(email),
                        "reference": "{}".format(walletNo),
                        "callbackUrl": "http://18.189.117.13:2011/test"}
                    responce = apis.DepositCard(data)
                    return redirect(responce["data"]["authurl"])
                else:
                    print("unspecified method")

            else:
                return render_template("/kite/chooseMethod.html", userdata=session["userdata"])
        except:
            return render_template("/kite/chooseMethod.html", userdata=session["userdata"])

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
        session["administrator"] = "maxmuthomi@gmail.com"
        return redirect("/Dashboard")
    else:
        session["administrator"] = "maxmuthomi@gmail.com"
        return redirect("/Dashboard")



@app.route("/Dashboard/")
def Dashboard():
    if "administrator" in session:
        tableData = ["Logs Table"]
        tableData.append(data.DashData())
        reqs = Numbers(data.DashData())
        return render_template("/adminPages/dashboard.html", dashboard="active", logs=tableData, cardsData=reqs)
    else:
        return redirect("/adminLogin")


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


def clever_function(date):
    convertedDate = fun.Convert(date)
    return convertedDate


app.jinja_env.globals.update(clever_function=clever_function)


@app.route("/forgot-password")
def ForgotPassword():
    return render_template("/kite/forgot-password.html")


if __name__ == "__main__":
    app.run(debug=True)