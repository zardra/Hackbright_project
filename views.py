from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from model import User, Image
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from flaskext.markdown import Markdown
import config
import forms
import model
import transform

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

@app.route("/directions")
@login_required
def go_to_images():
    filename = request.args.get("filename")
    filepath = "/static/uploads/" + filename
    
    # get id by removing ".png" from the filename
    file_id = filename.split(".")
    db_id = file_id[0]

    # get image from db based on id
    image = Image.query.get(db_id)

    # get the ws_rows value and send it to the transform functions
    if not image.directions:
        directions = transform.main(image.ws_rows)

        # save the directions to the database entry for the image
        image.directions = str(directions)
        model.session.commit()
    else:
        directions = eval(image.directions)

    return render_template("directions.html", filepath=filepath, directions=directions)


@app.route("/directions", methods=["POST"])
@login_required
def chart_directions():
    # pass the canvas image & the radio button selection
    img_data = request.form.get("img")
    button_val = request.form.get("buttonVal") 
    title = request.form.get("title")

    user = g.user
    user_id = user.id

    # create a new Image instance in the db
    image = Image(user_id=user_id, ws_rows=button_val, title=title)
    model.session.add(image)
    model.session.commit()
    model.session.refresh(image)

    # set the image's to a unique filename based on its db id
    img_filename = image.filename()
    filepath = "./static/uploads/" + img_filename

    # decode the canvas image into a png file
    png_file = open(filepath, "wb")
    png_file.write(img_data[22:].decode("base64"))
    png_file.close()
    return img_filename


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
