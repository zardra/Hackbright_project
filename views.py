from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from model import User, Image
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from flaskext.markdown import Markdown
import config
import forms
import model
import test

app = Flask(__name__)
app.config.from_object(config)

# Stuff to make login easier
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# End login stuff

# Adding markdown capability to the app
Markdown(app)

@app.before_request
def before_request():
    g.user = current_user

@app.route("/")
@login_required
def index():
    # posts = Post.query.all()
    return render_template("index.html")

@app.route("/allusers")
def allusers():
    # list all the users
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/allimages")
@login_required
def allimage():
    user = g.user
    user_id = user.id
    # list all the user's images
    images = Image.query.filter_by(user_id= user_id)
    return render_template("images.html", images=images)

@app.route("/imgtest")
@login_required
def go_to_images():
    filepath = request.args.get("filepath")
    directions = test.main("patterned")
    return render_template("imgtest.html", filepath=filepath, directions=directions)


@app.route("/imgtest", methods=["POST"])
@login_required
def imgtest():
    #pass the canvas image & the radio button selection
    imgData = request.form.get("img")
    buttonId = request.form.get("buttonId") #TODO: save value on image model, add title field as well!!!

    user = g.user
    user_id = user.id

    #create a new Image instance in the db
    image = Image(user_id=user_id)
    model.session.add(image)
    model.session.commit()
    model.session.refresh(image)

    #set the image's to a unique filename based on its db id
    imgfilename = image.filename()
    filepath = "./static/uploads/" + imgfilename

    #decode the canvas image into a png file
    png_file = open(filepath, "wb")
    png_file.write(imgData[22:].decode("base64"))
    png_file.close()
    return filepath


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def make_account():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    new_user = User(username=username, email=email)
    new_user.set_password(password=password)

    model.session.add(new_user)
    model.session.commit()
    model.session.refresh(new_user)
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate():
    form = forms.LoginForm(request.form)
    if not form.validate():
        flash("Incorrect username or password") 
        return render_template("login.html")

    username = form.username.data
    password = form.password.data

    user = User.query.filter_by(username=username).first()

    if not user or not user.authenticate(password):
        flash("Incorrect username or password") 
        return render_template("login.html")

    login_user(user)

    return redirect(request.args.get("next", url_for("index")))


if __name__ == "__main__":
    app.run(debug=True)
