from application import app, mongo
from flask import Response, json, render_template, request, redirect, flash, url_for
from application.templates.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        email = form.email.data
        password = form.password.data
        user_collection = User()
        user = user_collection.getUser(email=email)        
        if user and user_collection.get_password(user['password'] ,password):
            flash(f"{user['first_name']}, You are successfuly logged in!", "success")
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    return render_template("courses.html", courseData=courseData, courses=True, term=term)

@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_object = User()        
        user_id = len(user_object.getUsers())
        print(f"user_id={user_id}")
        user_id += 1

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        print(f"email={email}, password={password}, first_name={first_name}, last_name={last_name}")
        new_user = User(id=user_id, email=email, first_name=first_name, last_name=last_name)
        new_user.set_password(password=password)
        print(f"new_user={new_user}")
        new_user.save()
        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))

    return render_template("register.html", title="Register", form=form, register=True)

@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    id = request.form.get('courseID')
    title = request.form.get('title')
    term = request.form.get('term')
    return render_template("enrollment.html", enrollment=True, data={"id":id, "title":title, "term":term})

@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]
    
    return Response(json.dumps(jdata), mimetype="application/json")

@app.route("/user")
def user():
    # User(user_id=1, first_name='Prem', last_name="Kushwaha", email="prem@email.com", password="abc123").save()
    # User(user_id=2, first_name='Shayam', last_name="Kushwaha", email="shayam@email.com", password="pwd123").save()
    users = mongo.db.user.find()
    return render_template("user.html", users=users)