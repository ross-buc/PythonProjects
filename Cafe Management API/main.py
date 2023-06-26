"""
Python Flask API for managing cafes in a database using SQLAlchemy, RESTful principles and Flask.
"""
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET KEY"

##Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Cafe(db.Model):
    """
    Model representing the Cafe table in the database.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class AddForm(FlaskForm):
    """Create a form on the add page"""

    cafe_name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    has_power = SelectField(
        "Has Power?",
        choices=[("True", "Yes"), ("False", "No")],
        validators=[DataRequired()],
    )
    has_toilets = SelectField(
        "Has Toilets?",
        choices=[("True", "Yes"), ("False", "No")],
        validators=[DataRequired()],
    )
    has_wifi = SelectField(
        "Has Wifi?",
        choices=[("True", "Yes"), ("False", "No")],
        validators=[DataRequired()],
    )
    can_take_calls = SelectField(
        "Can take calls?",
        choices=[("True", "Yes"), ("False", "No")],
        validators=[DataRequired()],
    )
    seats = SelectField(
        "How many seats?",
        choices=[
            ("0-10", "0-10"),
            ("10-20", "10-20"),
            ("20-30", "20-30"),
            ("30-40", "30-40"),
            ("50+", "50+"),
        ],
        validators=[DataRequired()],
    )
    coffee_price = StringField("Coffee Price?", validators=[DataRequired()])
    submit = SubmitField("Add Cafe")


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """
    Home route for rendering the index.html template.
    """
    cafes = Cafe.query.all()

    return render_template("cafes.html", cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.cafe_name.data,
            map_url=form.map_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilets.data.lower() == "true",
            has_wifi=form.has_wifi.data.lower() == "true",
            has_sockets=form.has_power.data.lower() == "true",
            can_take_calls=form.can_take_calls.data.lower() == "true",
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    cafes = Cafe.query.all()
    if request.method == "POST":
        cafe_id = request.args.get("cafe_id")
        cafe_to_delete = Cafe.query.get(cafe_id)
        db.session.delete(cafe_to_delete)
        db.session.commit()
        print(cafe_to_delete)
        return redirect(url_for("home"))
    else:
        return render_template("delete.html", cafes=cafes)


if __name__ == "__main__":
    app.run(debug=True)
