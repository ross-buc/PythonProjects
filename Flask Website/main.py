"""
Authentication using Flask with werkzeug.security for hashed passwords
"""
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    send_from_directory,
)

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)

app = Flask(__name__)


app.config["SECRET_KEY"] = "any-secret-key-you-choose"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    email = request.form.get("email")
    if User.query.filter_by(email=email).first():
        flash(
            "You've already registered with that email address, sign in instead.",
            "error",
        )
        return render_template("login.html")
    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=8
        )
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Log in and authenticate user after adding details to database.
        login_user(new_user)
        return redirect(url_for("secrets", user=new_user.id))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Grab form information
        email = request.form.get("email")
        password = request.form.get("password")

        # Check for valid email
        if User.query.filter_by(email=email).first():
            user = User.query.filter_by(email=email).first()
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("secrets", user=user.id))
            flash("Password is incorrect", "error")
            return render_template("login.html")
        flash("Email doesn't exit in the database", "error")
        return render_template("login.html")
    return render_template("login.html")


@app.route("/secrets")
@login_required
def secrets():
    user_id = request.args.get("user")
    user = User.query.get(user_id)
    return render_template("secrets.html", user=user, logged_in=True)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/download")
@login_required
def download():
    return send_from_directory("static", filename="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
