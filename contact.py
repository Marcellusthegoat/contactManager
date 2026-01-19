
from flask import Flask,request,render_template,redirect,flash,session
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
# from passlib import sha256_crypt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://marcellusfieldridley:12345@cluster0.kxuyvqi.mongodb.net/projectcontact"
app.config["SECRET_KEY"] = "key"
mongo = PyMongo(app)

@app.route("/",  methods = ["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("Password")
        user = mongo.db.account.find_one({"USERNAME":username})
        # print(user)
        if user:
            print(user)
            # print(generate_password_hash(password),user[0]["PASSWORD"])
            # print(check_password_hash(password,user[0]["PASSWORD"]))
            if check_password_hash(user["PASSWORD"],password):
                session["username"] = username
                print('home')
                return(redirect('/home'))
    return render_template("contactlogin.html")

@app.route("/home", methods = ["POST","GET"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        contact = request.form.get("phone")
        if name != '' and contact != '':
            mongo.db.contacts.insert_one({"Name":name,"Contact":contact, "User":session["username"]})
        print(name,contact)
        return redirect('/home')
    data = mongo.db.contacts.find({"User":session["username"]})
    return render_template("contactmanager.html", contacts=data)

@app.route("/delete/<contactid>")
def deletecontact(contactid):
    mongo.db.contacts.delete_one({"_id":ObjectId(contactid)})
    return(redirect('/home'))



@app.route("/registration",  methods = ["POST","GET"])
def registration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("Password")
        data = list(mongo.db.account.find({"USERNAME":username}))
        print(data)
        if data:
            return(str(username) + " is already taken")
        else:
            mongo.db.account.insert_one({"USERNAME":username,"PASSWORD":generate_password_hash(password)})
            session["username"] = username
            return(redirect('/home'))
    return render_template("contactregistration.html")

@app.route("/update/<contactid>",methods = ["POST","GET"])
def update(contactid):
    if request.method == "POST":
        new_name = request.form.get("updateduser")
        new_number = request.form.get("updatedcontact")
    print(new_name,new_number)
    mongo.db.contacts.update_one(
        {"_id": ObjectId(contactid)},
        {"$set": {"Name": new_name, "Contact": new_number}}
    )
    print(contactid)
    return(redirect('/home'))



