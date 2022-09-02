from flask import Flask, render_template,request,redirect,url_for,session
import pymongo

app = Flask(__name__)

# configure secret key for session protection)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# MONGOGB DATABASE CONNECTION
connection_url = "mongodb://localhost:27017/"
client = pymongo.MongoClient(connection_url)
# client.list_database_names()
database_name = "Rently"
db = client[database_name]

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
    return render_template("search-car.html")

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
        db.users.insert_one({"name":name,"phone":phone,"email":email,"password":password})
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
        return redirect(url_for("userprofile"))

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('name', None)
    session.pop('email', None)
    # Redirect to index page
    return redirect(url_for('login'))

@app.route("/userprofile")
def userprofile():
    return render_template("userprofile.html")

@app.route("/mybookings")
def mybookings():
    return render_template("mybookings.html")

@app.route("/corporate-enquiries")
def corporate_enquiries():
    return render_template("corporate-enquiries.html")

@app.route("/book-now")
def book_now():
    return render_template("book-now.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

if __name__=='__main__':
    app.run(debug=True)