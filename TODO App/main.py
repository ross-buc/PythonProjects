"""
Python Flask API for managing TODOs in a database using SQLAlchemy, RESTful principles and Flask.
"""
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET KEY"

##Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Todo(db.Model):
    """
    Model representing the Todo table in the database.
    """

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(250), unique=False, nullable=False)
    priority = db.Column(db.String(250), unique=False, nullable=False)
    complete = db.Column(db.Boolean, nullable=False)


class AddTask(FlaskForm):
    """Create a form on the add page"""

    task = StringField("Task Description", validators=[DataRequired()])
    priority = SelectField(
        "Priority? ",
        choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Add Task")


with app.app_context():
    db.create_all()

# ADD INITIAL DATA TO DATABASE
# with app.app_context():
#     task = Todo(
#         task="Test",
#         priority="High",
#         complete=False,
#     )
#     db.session.add(task)
#     db.session.commit()


@app.route("/")
def home():
    """
    Home route for rendering the tasks.html template.
    """
    tasks = Todo.query.all()
    return render_template("tasks.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddTask()
    if form.validate_on_submit():
        new_task = Todo(
            task=form.task.data, priority=form.priority.data, complete=False
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        task_id = request.args.get("id")
        task_to_delete = Todo.query.get(task_id)
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/complete", methods=["GET", "POST"])
def complete():
    if request.method == "POST":
        task_id = request.args.get("id")
        task_to_complete = Todo.query.get(task_id)
        task_to_complete.complete = True
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
