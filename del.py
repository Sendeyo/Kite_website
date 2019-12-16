from flask import Flask, render_template, request, url_for, redirect, session, send_file
from werkzeug.utils import secure_filename
import os
import data

cwd = os.getcwd()



app = Flask(__name__)
app.secret_key = os.urandom(24)

# @app.route("/", methods = ["GET","POST"])
# def Login():
#     if "username" in session:
#         return redirect("/home")

#     if request.method == "POST":
#         attempted_email = request.form['email']
#         attempted_password = request.form['password']
#         user = fun.Authenticate(attempted_email, attempted_password)
#         if user:
#             session["username"] = user["Username"]
#             session["email"] = user["Email"]
#             session["category"] = user["Category"]
#             menu.clear()
#             menu.append(session['category'])
#             menu.append("logout")
#             return redirect("/home")
#         else:
#             return render_template("/login.html", error = "Wrong credentials")
#     else:
#         return render_template("/login.html")


@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def Registration():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm-password']
        if password == confirm:
            reg = fun.Register(username, email, password)
            if reg:
                return render_template("/register.html", error="This email exist")
            else:
                return render_template("/login.html", message="Account Created! now login")
        else:
            return render_template("/register.html", error="Password missmatch!")
    else:
        return render_template("/register.html")


@app.route("/")
def fake():
    return Home()


@app.route("/home")
def Home():
    return render_template("/home.html", user="Anonymax", tiles=menu)

# app.config["UPLOAD_FOLDER"] = "{}/static/uploads".format(cwd)

@app.route("/uploads/<string:name>", methods=["GET", "POST"])
def Upload(name):
    if request.method == "POST":
        if name == "members":
            validators = ['Member_no', 'National_id', 'Name',
                          'Station', 'Phone_no', 'Bank', 'Account_no']
            file_name = "members.xlsm"
            location = "static/uploads"

            file = request.files["file"]
            path = "static/uploads"
            filename = secure_filename(file.filename)
            file.save(os.path.join(path, filename))
            tempData = spreadsheet.Read(location, file_name, str(validators))
            session["tempData"] = tempData
            return render_template("/forms/register.html", rows=tempData, titles=validators, columns=len(validators))
    else:
        if name == "add":
            for row in session["tempData"]:
                number = row[0]
                id = row[1]
                name = row[2]
                station = row[3]
                phone = row[4]
                bank = row[5]
                account = row[6]
                querys = ['insert into Member_Basic_info (Member_no, National_id, Name, Station, Phone_no) values ("{}","{}","{}","{}","{}")'
                      .format(number, id, name, station, phone),
                       'insert into Member_Bank_info (Member_no, Bank, Bank_account) values("{}","{}","{}")'.format(number, bank, account)]
                print(account)
                data.data_write(querys[0])
                if bank:
                    data.data_write(querys[1])
            return render_template("/forms/register.html", message="Users Added Successfuly")

@app.route("/downloads/<string:name>")
def Download(name):
    try:
        if (name == "members"):
            filename = "members.xlsm"
            file = "{}/static/downloads/{}".format(cwd, filename)
            print(file)
            return send_file(file, attachment_filename="members.xlsm", as_attachment=True)
        elif (name == "collections"):
            spreadsheet.Create_collection_sheet()
            filename = "collection.xlsm"
            file = "{}/static/downloads/{}".format(cwd, filename)
            print(file)
            return send_file(file, attachment_filename="collection.xlsm", as_attachment=True)
    except:
        pass


tiles = ["Register Members","Pay Roll Generator"]
@app.route("/Admin/<string:name>", methods=["GET", "POST"])
def Admin(name):
    if name == "Register Members":
        if request.method == "POST":
            number = request.form["number"]
            id = request.form["id"]
            name = request.form["name"]
            station = request.form["station"]
            phone = request.form["phone"]
            bank = request.form["bank"]
            account = request.form["account"]
            querys = ['insert into Member_Basic_info (Member_no, National_id, Name, Station, Phone_no) values ("{}","{}","{}","{}","{}")'
                      .format(number, id, name, station, phone),
                       'insert into Member_Bank_info (Member_no, Bank, Bank_account) values("{}","{}","{}")'.format(number, bank, account)]
            print(account)
            data.data_write(querys[0])
            if bank:
                data.data_write(querys[1])
            return render_template("/forms/register.html", message = "Member Added successfully")

        return render_template("/forms/register.html")
    return render_template("/admin.html", tiles=tiles)



menu = ["Member Information", "Milk Collection", "Spreadsheet reader",
        "Loan information", "Admin Panel"]
@app.route("/home/<string:name>", methods=["GET", "POST"])
def Table(name):
    error = ""
    value = ""
    path = "/{}".format(name)
    if name == "Member Information":
        query = "select * from Member_Basic_info"
        if request.method == "POST":
            value = request.form['searched']
            query = "select * from Member_Basic_info where Name like '%{}%'".format(value)
        everyone = data.read(query)
        columns = 6
        titles = ["Member Number", "National Id",
                  "Member Name", "Member Station", "Phone number"]
        if not everyone:
            error = "{} Does not exist".format(value.title())

        return render_template("/table.html", columns=columns, rows=everyone, titles=titles, error=error, path=path)
    elif name == "Milk Collection":
        return redirect("/{}".format(name))
    elif name == "Admin Panel":
        return render_template("/admin.html", tiles=tiles)
    else:
        return ("Nothing")

    return "asdfghj"

@app.route("/Milk Collection")
def Collection():
    
    return render_template("/collection.html")

@app.route("/{}/<int:id>".format(menu[0]))
def Details(id):
    return render_template("/member.html")


if __name__ == "__main__":
    app.run(debug=True)
