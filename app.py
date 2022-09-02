from flask import Flask, render_template

app = Flask(__name__)

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

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

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