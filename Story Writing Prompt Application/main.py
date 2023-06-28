"""
Python Flask App that prompts a user with a story idea. Once the user starts typing, they have 10 seconds before the
text field will disable unless they type another word. This is a good way of working through writers block by applying
a pressured environment to type within
"""
import random
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET KEY"

##Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///AppDatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Bootstrap(app)

# Some random writing prompts
prompts = [
    "In an unexpected adventure, a secret note revealed itself.",
    "On an ordinary street, a magical door stood mysteriously.",
    "Without a map, I found myself lost in a foreign city.",
    '"I never thought I\'d see you again," she whispered, her voice filled with disbelief.',
    "A knock on the door interrupted my day as a mysterious package arrived.",
    "As the clock struck thirteen, the world around me transformed.",
    '"Where were you?" he asked, his voice filled with concern.',
    "In the depths of the old attic, a hidden treasure awaited discovery.",
    "The abandoned house stood silently, holding its haunting secret.",
    "Memories long forgotten resurfaced unexpectedly, flooding my mind.",
    "I felt a chill in the air as I encountered the ghostly figure.",
    "A chance encounter at the café led to an unexpected friendship.",
    "With the first snowfall, consequences unfolded beyond imagination.",
    "The pen, mightier than the sword, shaped destinies with each stroke.",
    "A knock on the door shattered the silence, signaling a fateful arrival.",
    "As I gazed at the photograph, my heart skipped a beat.",
    "Inside the old bookstore, a portal to another world beckoned.",
    "Waking up in a different body, confusion consumed my thoughts.",
    "Against all odds, their love burned fiercely, defying societal boundaries.",
    "The mirror reflected a distorted reality, revealing hidden truths.",
    "Unbeknownst to me, I possessed a unique superpower within.",
    "With the final page missing, the book's ending remained a mystery.",
    "In the hazy twilight of my dreams, a story began to unfold.",
    "The map, found amidst dust and cobwebs, pointed to buried treasure.",
    "With excitement bubbling within, a secret note unveiled a joyful adventure.",
    "Along an ordinary street, a magical door beamed with enchantment.",
    "Exploring a foreign city without a map turned into an exhilarating journey of discovery.",
    '"I never thought I\'d see you again!" she exclaimed, a smile spreading across her face.',
    "A knock on the door brought unexpected delight as a mysterious package arrived.",
    "As the clock struck thirteen, a wave of serendipity swept through the air.",
    '"Guess what happened today?" he exclaimed, eager to share his story.',
    "Amidst the old attic, a hidden treasure sparkled, promising joy and wonder.",
    "The abandoned house, once forgotten, revealed its history with a sense of nostalgia.",
    "Memories long forgotten resurfaced unexpectedly, filling my heart with warmth.",
    "I felt a gentle presence in the room as I encountered the friendly ghostly figure.",
    "A chance encounter at the café blossomed into a heartwarming friendship.",
    "With the first snowfall, laughter filled the air, creating magical moments.",
    "The pen, mightier than the sword, weaved tales of inspiration and happiness.",
    "A knock on the door signaled the arrival of loved ones, bringing joy and anticipation.",
    "As I gazed at the photograph, a flood of fond memories washed over me.",
    "Inside the old bookstore, a portal to imagination invited smiles and wonder.",
    "Waking up in a different body turned out to be a delightful adventure of self-discovery.",
    "Against all odds, their love defied boundaries, bringing pure happiness to their lives.",
    "The mirror reflected a radiant reality, highlighting beauty and self-acceptance.",
    "Unbeknownst to me, I possessed a unique superpower to spread joy and kindness.",
    "With the final page missing, the book's ending remained open, filled with endless possibilities.",
    "In the hazy twilight of my dreams, a delightful story began to unfold.",
    "The map, found amidst dust and cobwebs, led to a treasure of cherished memories.",
    "As the carnival rolled into town, laughter and excitement filled the air, igniting happiness in everyone's hearts.",
]


class Prompts(db.Model):
    """
    Model representing the Prompts table in the database.
    """

    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(250), nullable=False)


class SavedStories(db.Model):
    """
    Model representing the Prompts table in the database.
    """

    id = db.Column(db.Integer, primary_key=True)
    users_prompt = db.Column(db.String(250), nullable=False)
    saved_text = db.Column(db.String(100000), nullable=False)


with app.app_context():
    db.create_all()

# Initial setup of DB
# with app.app_context():
#     # Delete existing prompts
#     db.session.query(Prompts).delete()
#     db.session.commit()

#     # Add new prompts
#     for prompt_text in prompts:
#         prompt = Prompts(prompt=prompt_text)
#         db.session.add(prompt)
#     db.session.commit()

# with app.app_context():
#     db.session.query(SavedStories).delete()
#     new_story = SavedStories(
#         users_prompt="This is the first prompt",
#         saved_text="This is follow up text from the prompt",
#     )
#     db.session.add(new_story)
#     db.session.commit()


@app.route("/")
def home():
    """
    Home route for rendering the tasks.html template.
    """
    prompts = Prompts.query.all()
    random_prompt = random.choice(prompts)
    return render_template("typing.html", random_prompt=random_prompt)


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        user_input = request.form.get("user_input_hidden")
        users_prompt = request.form.get("prompt")
        new_story = SavedStories(
            users_prompt=users_prompt,
            saved_text=user_input,
        )
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/saved", methods=["GET", "POST"])
def saved():
    stories = SavedStories.query.all()
    return render_template("saved.html", stories=stories)


if __name__ == "__main__":
    app.run(debug=True)
