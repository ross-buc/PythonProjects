"""
Python Flask API for managing cafes in a database using SQLAlchemy, RESTful principles, and JSON responses.
"""
import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

##Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    """
    Model representing the Cafe table in the database.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """
    Home route for rendering the index.html template.
    """
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def random_cafe():
    """
    GET route to retrieve a random cafe from the database.
    """
    if request.method == "GET":
        random_cafe = random.choice(Cafe.query.all())
        print(random_cafe)
        return jsonify(cafe=random_cafe.name, seats=random_cafe.seats)
    else:
        return render_template("index.html")


@app.route("/all", methods=["GET"])
def all_cafes():
    """
    GET route to retrieve all cafes from the database.
    """
    if request.method == "GET":
        cafes = Cafe.query.all()
        cafes_dict = [
            dict(
                (column.name, getattr(cafe, column.name))
                for column in Cafe.__table__.columns
            )
            for cafe in cafes
        ]
        return jsonify(cafe=cafes_dict)
    else:
        return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    """
    POST route to add a new cafe to the database.
    """
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new cafe."})
    else:
        return render_template("index.html")


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def patch(cafe_id):
    """
    PATCH route to update the coffee price of a specific cafe in the database.
    """
    if request.method == "PATCH":
        print(cafe_id)
        cafe_to_edit = Cafe.query.get(cafe_id)
        if cafe_to_edit:
            new_price = request.args.get("price")
            cafe_to_edit.coffee_price = new_price
            db.session.commit()
            return jsonify(
                response={"success": "Successfully updated the cafe's coffee price."}
            )
        else:
            return jsonify(
                error={
                    "Not Found": "Sorry a cafe with that ID was not found in the database."
                }
            )
    else:
        return render_template("index.html")


@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    """
    DELETE route to delete a specific cafe from the database if the API-KEY is correct.
    """
    if request.method == "DELETE":
        cafe_to_delete = Cafe.query.get(cafe_id)
        API_KEY = "TopSecretAPIKey"
        user_api_key = request.args.get("api-key")
        if user_api_key != API_KEY:
            return jsonify(error={"Wrong API KEY": "Please enter a valid API KEY."})

        if not cafe_to_delete:
            return jsonify(
                error={
                    "Not Found": "Sorry, a cafe with that ID was not found in the database."
                }
            )
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe."})
    else:
        return render_template("index.html")


@app.route("/search", methods=["GET"])
def search():
    """
    GET route to search for cafes at a specific location in the database.
    """
    location = request.args.get("loc")
    if request.method == "GET":
        cafes = Cafe.query.all()
        cafes_at_location = []
        for cafe in cafes:
            if cafe.location == location:
                cafes_at_location.append(cafe)
        cafes_dict = [
            dict(
                (column.name, getattr(cafe, column.name))
                for column in Cafe.__table__.columns
            )
            for cafe in cafes_at_location
        ]
        if cafes_dict:
            return jsonify(cafe=cafes_dict)
        else:
            return jsonify(
                error={"Not Found": "Sorry, we don't have a cafe at that location"}
            )
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
