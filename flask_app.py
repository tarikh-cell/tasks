
# A very simple Flask Hello World app for you to get started with...
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="TMCell",
    password="p77h9bSJfv7h:sw",
    hostname="TMCell.mysql.eu.pythonanywhere-services.com",
    databasename="TMCell$Tasks",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Status(Enum):
    READY = "Ready"
    INPROGRESS = "In Progress"
    COMPLETED = "Completed"

class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(4096))
    description = db.Column(db.String(4096))
    status = db.Column(db.Enum(Status))
    due_date = db.Column(db.DateTime, default=datetime.now)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = Task(title = request.form["title"], description = request.form["description"], status = Status[request.form["status"]])
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', tasks=Task.query.all())

@app.route("/<int:task_id>", methods=["PUT", "DELETE"])
def update_task(task_id):
    if request.method == "PUT":
        task = Task.query.get_or_404(task_id)
        data = request.json
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        if "status" in data:
            task.status = Status[data["status"]]  # again, use enum name
        if "due_date" in data:
            task.due_date = datetime.fromisoformat(data["due_date"])
    elif request.method == "DELETE":
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))