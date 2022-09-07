from ast import withitem
from flask import Flask, render_template,request,redirect,url_for,session
import pymongo
import os
from os.path import join, dirname, realpath
from PIL import Image
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

app = Flask(__name__)

# configure secret key for session protection)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# MONGOGB DATABASE CONNECTION
connection_url = "mongodb://localhost:27017/"
client = pymongo.MongoClient(connection_url)
# client.list_database_names()
database_name = "Rently"
db = client[database_name]

CARS_FOLDER = join(dirname(realpath(__file__)), 'static/images/cars')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg',}
app.config['CARS_FOLDER'] = CARS_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/our-clients")
def our_clients():
    return render_template("our-clients.html")

@app.route("/search-car")
def search_car():
    data = db.cars.find()
    cars = []
    for i in data:
        i.update({"_id":str(i["_id"])})
        cars.append(i)

    return render_template("search-car.html",cars=cars)

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        password = request.form.get("password")
        # check if exists 
        phone_exist = db.users.find_one({"phone":phone})
        email_exist = db.users.find_one({"email":email})
        if phone_exist:
            e="Phone Number Already Registered!"
            return render_template("signup.html",error=e)
        if email_exist:
            e="Email Address Already Registered!"
            return render_template("signup.html",error=e)
        db.users.insert_one({"name":name,"phone":phone,"email":email,"password":password,"user_type":"user"})
        return render_template("login.html",success="Account Created Succesfully!")
    return render_template("signup.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get("email")
        password = request.form.get("password")
        # check 
        
        exist = db.users.find_one({"email":email})
        if not exist:
            e="Invalid Email!"
            return render_template("login.html",error=e)
        if exist['password']!=password:
            e="Invalid Password!"
            return render_template("login.html",error=e)
        session['loggedin'] = True
        session['userid'] = str(exist["_id"])
        session['name'] = exist["name"]
        session['email'] = exist["email"]
        session['type'] == exist['user_type']
        return redirect(url_for("userprofile"))

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    try:
        tmp = session['type']
        session.pop('loggedin', None)
        session.pop('userid', None)
        session.pop('name', None)
        session.pop('email', None)
        session.pop('type', None)
        if tmp == "admin":
            return redirect(url_for("admin_login"))
        else:
            return redirect(url_for('login'))
    except:
        pass

@app.route("/userprofile")
def userprofile():
    return render_template("userprofile.html")

@app.route("/mybookings")
def mybookings():
    return render_template("mybookings.html")

@app.route("/corporate-enquiries",methods=['GET','POST'])
def corporate_enquiries():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        number = request.form.get("number")
        address = request.form.get("address")
        location = request.form.get("location")
        cars = request.form.get("cars")
        days = request.form.get("days")
        purpose = request.form.get("purpose")
        details = request.form.get("details")
        db.corporate_inquiries.insert_one({
            "name":name,
            "email":email,
            "number":number,
            "address":address,
            "location":location,
            "cars":cars,
            "days":days,
            "purpose":purpose,
            "details":details
        })
        return render_template("corporate-enquiries.html",success=True)


    return render_template("corporate-enquiries.html")


@app.route("/book-now/<string:id>/<string:type>",methods=['GET','POST'])
def book_now(id,type):
    if request.method == 'POST':
        pickup_date = request.form.get("pickup_date")
        pickup_time = request.form.get("pickup_time")
        pickup_location = request.form.get("pickup_location")
        pickup_desc = request.form.get("pickup_desc")
        dropoff_location = request.form.get("dropoff_location")
        dropoff_desc = request.form.get("dropoff_desc")
        print(pickup_date)
        print(pickup_time)
        print(pickup_location)
        print(pickup_desc)
        print(dropoff_location)
        print(dropoff_desc  )
        return "booked"
    type = type.replace("_"," ")
    car = db.cars.find_one({"_id":ObjectId(id)})
    car = car.update({"_id":str(car["_id"])})
    return render_template("book-now.html",type=type,car_id=id,car=car)

@app.route("/blog")
def blog():
    return render_template("blog.html")

# -x-x-x-x-x-x ADMIN DASH -x-x-x-x-x-x
@app.route("/admin")
def admin():
    if 'loggedin' in session:
        if session['type'] == 'admin':
            return render_template("admin-index.html",username=session['name'])
        else:
            return redirect(url_for("admin_login"))
    else:
        return redirect(url_for("admin_login"))

@app.route("/admin-login",methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        exist = db.users.find_one({"email":email,"user_type":"admin"})
        print(exist)
        if exist:
            if password == exist['password']:
                # Let him login now as admin
                session['loggedin'] = True
                session['userid'] = str(exist["_id"])
                session['name'] = exist["name"]
                session['email'] = exist["email"]
                session['type'] = exist["user_type"]
                return redirect(url_for("admin"))
            else:
                return render_template("admin-login.html",error="Invalid Password!")
        else:
            return render_template("admin-login.html",error="Invalid Email!")

    if 'loggedin' in session:
        if session['type'] == 'admin':
            return redirect(url_for("admin"))
        else:
            return render_template("admin-login.html",error="Please Logout From User Account First!")
    else:
        return render_template("admin-login.html")

@app.route("/registered-vehicles")
def registered_vehicles():
    if 'loggedin' in session:
        if session['type'] == 'admin':
            data = db.cars.find()
            cars = []
            for i in data:
                i.update({"_id":str(i["_id"])})
                cars.append(i)
            return render_template("registered-vehicles.html",cars=cars,username=session['name'])
        else:
            return render_template("admin-login.html",error="Please Logout From User Account First!")
    else:
        return render_template("admin-login.html")

@app.route("/add-vehicle",methods=['GET','POST'])
def add_vehicle():
    if request.method == 'POST':
        name = request.form.get("name")
        price_per_day = float(request.form.get("price_per_day"))
        city = request.form.get("city")
        with_driver = request.form.get("with_driver")
        if with_driver == "true":
            with_driver = True
        elif with_driver == "false":
            with_driver == False
        ac = request.form.get("ac")
        if ac == "true":
            ac = True
        elif ac == "false":
            ac = False
        doors = int(request.form.get("doors"))
        transmission = request.form.get("transmission")
        overtime = float(request.form.get("overtime"))
        fuel_average = float(request.form.get("fuel_average"))
        full_day = int(request.form.get("full_day"))
        if 'pic' not in request.files:
            pic = None
        else:
            pic = request.files['pic']

        if pic and allowed_file(pic.filename):
                filename = secure_filename(pic.filename)
                pic.save(os.path.join(CARS_FOLDER, filename))
        print(name)
        print(price_per_day)
        print(city)
        print(with_driver)
        print(ac)
        print(doors)
        print(transmission)
        print(overtime)
        print(fuel_average)
        print(full_day)
        db.cars.insert_one({
            "name":name,
            "price_per_day":price_per_day,
            "city":city,
            "with_driver":with_driver,
            "ac":ac,
            "doors":doors,
            "transmission":transmission,
            "overtime":overtime,
            "fuel_average":fuel_average,
            "full_day":full_day,
            "pic":pic.filename
        })
        return redirect(url_for("registered_vehicles"))
    if 'loggedin' in session:
        if session['type'] == 'admin':
            return render_template("add-vehicle.html",username=session['name'])
        else:
            return render_template("admin-login.html",error="Please Logout From User Account First!")
    else:
        return render_template("admin-login.html")


@app.route("/edit-registered-vehicle/<string:id>",methods=['GET','POST'])
def edit_registered_vehicle(id):
    if request.method == 'POST':
        name = request.form.get("name")
        price_per_day = float(request.form.get("price_per_day"))
        city = request.form.get("city")
        with_driver = request.form.get("with_driver")
        if with_driver == "true":
            with_driver = True
        elif with_driver == "false":
            with_driver == False
        ac = request.form.get("ac")
        if ac == "true":
            ac = True
        elif ac == "false":
            ac = False
        doors = int(request.form.get("doors"))
        transmission = request.form.get("transmission")
        overtime = float(request.form.get("overtime"))
        fuel_average = float(request.form.get("fuel_average"))
        full_day = int(request.form.get("full_day"))
        if 'pic' not in request.files:
            pic = None
        else:
            pic = request.files['pic']
        

        if pic and allowed_file(pic.filename):
                filename = secure_filename(pic.filename)
                pic.save(os.path.join(CARS_FOLDER, filename))
        
        # Values to be updated.
        filter = { "_id": ObjectId(id) }
        if pic: 
            new_values = {
                '$set': {
                    "name": name,
                    "price_per_day": price_per_day,
                    "city": city,
                    "with_driver": with_driver,
                    "ac": ac,
                    "doors": doors,
                    "transmission": transmission,
                    "overtime": overtime,
                    "fuel_average":fuel_average,
                    "full_day": full_day,
                    "pic": pic.filename
                }
            }
        else: 
            new_values = {
                '$set': {
                    "name": name,
                    "price_per_day": price_per_day,
                    "city": city,
                    "with_driver": with_driver,
                    "ac": ac,
                    "doors": doors,
                    "transmission": transmission,
                    "overtime": overtime,
                    "fuel_average":fuel_average,
                    "full_day": full_day,
                }
            }
        db.cars.update_one(filter, new_values)
        return redirect(url_for("registered_vehicles"))
    if 'loggedin' in session:
        if session['type'] == 'admin':
            car = db.cars.find_one({"_id":ObjectId(id)})
            full_day = [8,12,24]
            return render_template("edit-vehicle.html",username=session['name'],car=car,full_day=full_day)
        else:
            return render_template("admin-login.html",error="Please Logout From User Account First!")
    else:
        return render_template("admin-login.html")

@app.route("/delete-registered-vehicle/<string:id>",methods=['GET'])
def delete_registered_vehicle(id):
    if 'loggedin' in session:
        if session['type'] == 'admin':
            query = {"_id":ObjectId(id)}
            exist = db.cars.find_one(query)
            if not exist:
                return str("Invalid Vehicle Id.. Or vehicle does not exist anymore")
            deleted = exist['name'] + " Deleted Successfully!"
            db.cars.delete_one(query)
            data = db.cars.find()
            cars = []
            for i in data:
                i.update({"_id":str(i["_id"])})
                cars.append(i)
            return render_template("registered-vehicles.html",cars=cars,username=session['name'],deleted=deleted)
        else:
            return render_template("admin-login.html",error="Please Logout From User Account First!")
    else:
        return render_template("admin-login.html")

@app.route("/test")
def test():
    return render_template("test.html")





if __name__=='__main__':
    app.run(debug=True)